#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from time import sleep

import dask.dataframe as dd

from swagit_dataset_generator import SwagitScraper

###############################################################################

checks = 1
previous_oldest = None
previous_newest = None
previous_counts = None
while True:
    # Wipe stdout
    os.system("cls" if os.name == "nt" else "clear")

    # Read
    print(f"Check: {checks}")
    print("")
    df = dd.read_parquet(f"{SwagitScraper.DEFAULT_STORAGE_DIR}/*")

    # Compute dates
    new_oldest = df.meeting_datetime.min().compute()
    new_newest = df.meeting_datetime.max().compute()
    if previous_oldest:
        diff_oldest = previous_oldest - new_oldest
        diff_newest = previous_newest - new_newest
    else:
        diff_oldest = 0
        diff_newest = 0
    print(
        f"Date range: "
        f"{new_oldest} - {new_newest} "
        f"(oldest change: {diff_oldest}, newest change: {diff_newest})"
    )
    previous_oldest = new_oldest
    previous_newest = new_newest

    # Line break
    print("")

    # Counts
    new_counts = df.municipality.value_counts().compute()
    print(f"Municipality counts:\n{new_counts}")
    if previous_counts is not None:
        print("")
        diff_counts = new_counts.sub(previous_counts, fill_value=0)
        print(f"Counts change:\n{diff_counts}")
    previous_counts = new_counts

    # Wait 3 minutes
    checks += 1
    sleep(180)
