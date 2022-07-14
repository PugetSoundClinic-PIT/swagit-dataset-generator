#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Optional, Union

import requests
from bs4 import BeautifulSoup
from dataclasses_json import DataClassJsonMixin
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
    INDEX_FILENAME = "current_index.txt"

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
        start_index: int,
        end_index: int = 200_000,
        batch_size: int = 100,
        storage_dir: Union[str, Path] = DEFAULT_STORAGE_DIR,
        workers: Optional[int] = None,
    ) -> None:
        # Store params
        self.start_index = start_index
        self.end_index = end_index
        self.batch_size = batch_size
        self.storage_dir = storage_dir
        self.workers = workers

        # Store general state
        self.current_index = start_index

    @staticmethod
    def _process_page(
        index: int,
        trial: int = 0,
        max_trials: int = 3,
    ) -> Optional[SwagitPageParse]:
        # Get the page
        url = SwagitScraper.BASE_URI_PATTERN.format(index=index)
        log.debug(f"Fast checking: '{url}'")
        response = requests.get(url)

        # Check status and backoff retry
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if trial < max_trials:
                sleep(4**trial)
                return SwagitScraper._process_page(
                    index=index,
                    trial=trial + 1,
                    max_trials=max_trials,
                )
            else:
                # Open log file and store current index
                raise e

        # Parse title
        soup = BeautifulSoup(response.text, "html.parser")
        match_or_none = re.match(SwagitScraper.TITLE_RE_COMPILED, soup.title.string)

        # Check content
        if match_or_none is None:
            return None

        # Construct datetime
        month = match_or_none.group(1)
        day = match_or_none.group(3)
        year = match_or_none.group(5)
        body = match_or_none.group(7)
        municipality = match_or_none.group(9)
        dt = datetime.strptime(f"{month} {day} {year}", "%b %d %Y")

        return SwagitPageParse(
            _i=index,
            municipality=municipality,
            meeting_body=body,
            meeting_datetime=dt,
        )

    def run(self) -> None:
        # Determine number of batches

        # Run batches

        # Run pages

        # Store batch

        # Update log file
        pass
