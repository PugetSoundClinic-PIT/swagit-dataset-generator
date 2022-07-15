# swagit-dataset-generator

[![Build Status](https://github.com/PugetSoundClinic-PIT/swagit-dataset-generator/workflows/Build/badge.svg)](https://github.com/PugetSoundClinic-PIT/swagit-dataset-generator/actions)
[![Documentation](https://github.com/PugetSoundClinic-PIT/swagit-dataset-generator/workflows/Documentation/badge.svg)](https://PugetSoundClinic-PIT.github.io/swagit-dataset-generator)

A small package to generate a dataset of municipal council meeting metadata from Swagit.

---

## Installation

**Stable Release:** `pip install swagit-dataset-generator`<br>
**Development Head:** `pip install git+https://github.com/PugetSoundClinic-PIT/swagit-dataset-generator.git`

## Quickstart

```python
from swagit_dataset_generator import SwagitScraper
import dask.dataframe as dd

scraper = SwagitScraper(start_index=10000, end_index=10100, batch_size=10)
chunks_dir = scraper.run()

results_df = dd.read_parquet(f"{chunks_dir}/*")
print(results_df.meeting_body.value_counts().compute())
```

## Documentation

For full package documentation please visit [PugetSoundClinic-PIT.github.io/swagit-dataset-generator](https://PugetSoundClinic-PIT.github.io/swagit-dataset-generator).

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for information related to developing the code.

For development commands we use [just](https://github.com/casey/just).

```bash
just
```
```
Available recipes:
    build                    # run tox / run tests and lint
    clean                    # clean all build, python, and lint files
    default                  # list all available commands
    generate-docs            # generate Sphinx HTML documentation
    lint                     # lint, format, and check all files
    serve-docs               # generate Sphinx HTML documentation and serve to browser
    update-from-cookiecutter # update this repo using latest cookiecutter-py-package
```

**MIT License**
