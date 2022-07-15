#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import sys
import traceback

import numpy as np

from swagit_dataset_generator import SwagitScraper

###############################################################################


class Args(argparse.Namespace):
    def __init__(self) -> None:
        self.__parse()

    def __parse(self) -> None:
        p = argparse.ArgumentParser(
            prog="sample-swagit-dataset",
            description="Run a sampled Swagit dataset generation.",
        )
        p.add_argument(
            "low",
            type=int,
            help="The integer low value to sample between.",
        )
        p.add_argument(
            "high",
            type=int,
            help="The integer high value to sample between.",
        )
        p.add_argument(
            "-s",
            "--sample",
            type=float,
            default=0.2,
            dest="sample",
            help="The percent to sample between the start and end indices.",
        )
        p.add_argument(
            "--debug",
            dest="debug",
            action="store_true",
            help="Run with debug logging.",
        )
        p.parse_args(namespace=self)


def main() -> None:
    # Get args
    args = Args()

    # Determine log level
    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    # Setup logging
    logging.basicConfig(
        level=log_level,
        format="[%(levelname)4s: %(module)s:%(lineno)4s %(asctime)s] %(message)s",
    )
    log = logging.getLogger(__name__)

    # Process
    try:
        # Generate indices
        np.random.seed(12)
        possible = np.arange(args.low, args.high)
        sample_size = int(args.sample * (args.high - args.low))
        sampled = np.random.choice(possible, size=sample_size, replace=False).tolist()
        log.debug(f"Swagit indices to process: {len(sampled)}")

        # Run
        scraper = SwagitScraper()
        scraper.run(indices=sampled)

    except Exception as e:
        log.error("=============================================")
        log.error("\n\n" + traceback.format_exc())
        log.error("=============================================")
        log.error("\n\n" + str(e) + "\n")
        log.error("=============================================")
        sys.exit(1)


###############################################################################
# Allow caller to directly run this module (usually in development scenarios)

if __name__ == "__main__":
    main()
