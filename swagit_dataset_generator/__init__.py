# -*- coding: utf-8 -*-

"""Top-level package for swagit_dataset_generator."""

__author__ = "Eva Maxfield Brown"
__email__ = "evamaxfieldbrown@gmail.com"
# Do not edit this string manually, always use bumpversion
# Details in CONTRIBUTING.md
__version__ = "0.0.0"


def get_module_version() -> str:
    return __version__


from .swagit_scraper import SwagitScraper  # noqa: F401
