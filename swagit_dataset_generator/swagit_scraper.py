#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import math
import re
from dataclasses import dataclass
from datetime import datetime
from functools import partial
from pathlib import Path
from time import sleep
from typing import List, Optional, Union

import pandas as pd
import requests
from bs4 import BeautifulSoup
from dataclasses_json import DataClassJsonMixin
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

###############################################################################

log = logging.getLogger(__name__)

###############################################################################


@dataclass
class SwagitPageParse(DataClassJsonMixin):
    _i: int
    municipality: str
    meeting_body: str
    meeting_datetime: datetime


###############################################################################


class SwagitScraper:

    BASE_URI_PATTERN = "https://houstontx.new.swagit.com/videos/{index}"
    DEFAULT_STORAGE_DIR = Path("swagit-dataset-chunks")

    # Match pattern of
    # Any character one to unlimited times
    # Then a whitespace character
    # Then any character one to unlimited times
    # Then a comma and whitespace
    # Then four digits
    # Then a white space
    # Then any character one to unlimited times
    # Then a whitespace, a hyphen, and a whitespace
    # Finally, any character one to unlimited times
    # Examples:
    # Sep 12, 2007 Board Briefing - Dallas ISD, TX
    # Oct 24, 2007 Board Meeting - Dallas ISD, TX
    # Jun 26, 2013 Regular - Tamarac, FL
    TITLE_REGEX = r"^(.+)(\s)(.+)(\,\s)([0-9]{4})(\s)(.+)(\s\-\s)(.+)$"
    TITLE_RE_COMPILED = re.compile(TITLE_REGEX)

    def __init__(
        self,
        start_index: int = 0,
        end_index: int = 200_000,
        batch_size: int = 100,
        storage_dir: Union[str, Path] = DEFAULT_STORAGE_DIR,
        workers: Optional[int] = 4,
        max_trials_per_page: int = 3,
        time_per_request: int = 3,
    ) -> None:
        # Store params
        self.start_index = start_index
        self.end_index = end_index
        self.batch_size = batch_size
        self.storage_dir = Path(storage_dir)
        self.workers = workers
        self.max_trials_per_page = max_trials_per_page
        self.time_per_request = time_per_request

        # Store general state
        self.current_index = start_index

        # Create storage dir
        self.storage_dir.mkdir(exist_ok=True, parents=True)

    @staticmethod
    def _process_page(
        index: int,
        trial: int = 0,
        max_trials: int = 3,
        time_per_request: int = 3,
    ) -> Optional[SwagitPageParse]:
        # Get the page
        url = SwagitScraper.BASE_URI_PATTERN.format(index=index)
        log.debug(f"Requesting: '{url}'")
        response = requests.get(url)

        # Check status and backoff retry
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if trial < max_trials:
                sleep_seconds = 8**trial
                log.debug(f"Retrying '{url}' in {sleep_seconds} seconds...")
                sleep(sleep_seconds)
                return SwagitScraper._process_page(
                    index=index,
                    trial=trial + 1,
                    max_trials=max_trials,
                )
            else:
                log.debug(f"Failed to parse '{url}' after multiple attempts, skipping.")
                return None

        # Parse title
        soup = BeautifulSoup(response.text, "html.parser")
        match_or_none = re.match(SwagitScraper.TITLE_RE_COMPILED, soup.title.string)

        # Check content
        if match_or_none is None:
            log.debug(f"Could not match title from '{url}', skipping.")
            return None

        # Construct datetime
        try:
            month = match_or_none.group(1)
            day = match_or_none.group(3)
            year = match_or_none.group(5)
            body = match_or_none.group(7)
            municipality = match_or_none.group(9)
            dt = datetime.strptime(f"{month} {day} {year}", "%b %d %Y")
        except Exception:
            log.debug(f"Could not parse title: '{soup.title.string}'")
            return None

        # Wait to limit ourselves
        sleep(time_per_request)

        return SwagitPageParse(
            _i=index,
            municipality=municipality,
            meeting_body=body,
            meeting_datetime=dt,
        )

    def run(self, indices: Optional[List[int]] = None) -> Path:
        # Determine number of batches
        if indices is None:
            total_n = self.end_index - self.start_index
        else:
            total_n = len(indices)

        batches = math.ceil(total_n / self.batch_size)

        # Run batches
        process_func = partial(
            self._process_page,
            max_trials=self.max_trials_per_page,
            time_per_request=self.time_per_request,
        )
        for _ in tqdm(range(batches), "Batches"):
            try:
                if indices:
                    results = thread_map(
                        process_func,
                        indices[
                            self.current_index : self.current_index + self.batch_size
                        ],
                        max_workers=self.workers,
                        desc="This Batch",
                    )
                else:
                    results = thread_map(
                        process_func,
                        range(self.current_index, self.current_index + self.batch_size),
                        max_workers=self.workers,
                        desc="This Batch",
                    )
            except Exception as e:
                log.error(f"Stopped at index: {self.current_index}")
                raise e

            # Filter nones
            results = [r.to_dict() for r in results if r is not None]
            results_df = pd.DataFrame(results)
            result_store_path = self.storage_dir / f"{self.current_index}.parquet"
            results_df.to_parquet(result_store_path)
            log.debug(f"Stored chunk to: '{result_store_path}'")
            self.current_index += self.batch_size

        return self.storage_dir
