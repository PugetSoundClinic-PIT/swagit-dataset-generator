# swagit-dataset-generator

[![Build Status](https://github.com/evamaxfield/swagit-dataset-generator/workflows/Build/badge.svg)](https://github.com/evamaxfield/swagit-dataset-generator/actions)
[![Documentation](https://github.com/evamaxfield/swagit-dataset-generator/workflows/Documentation/badge.svg)](https://swagit-dataset-generator.github.io/swagit-dataset-generator)

A small package to generate a dataset of municipal council meeting metadata from Swagit.

---

## Setting Up the Repo

1. Turn your project into a GitHub repository:
    - Make an account on [github.com](https://github.com)
    - Go to [make a new repository](https://github.com/new)
    - _Recommendations:_
        - _It is strongly recommended to make the repository name the same as the Python
            package name_
        - _A lot of the following optional steps are *free* if the repository is Public,
            plus open source is cool_
    - After a GitHub repo has been created, run the commands listed under:
        "...or push an existing repository from the command line"
2. Ensure that you have set GitHub pages to build the `gh-pages` branch by selecting the
   `gh-pages` branch in the dropdown in the "GitHub Pages" section of the
   repository settings.
   ([Repo Settings](https://github.com/evamaxfield/swagit-dataset-generator/settings))
3. Register your project with PyPI:
    - Make an account on [pypi.org](https://pypi.org)
    - Go to your GitHub repository's settings and under the
      [Secrets tab](https://github.com/evamaxfield/swagit-dataset-generator/settings/secrets/actions),
      add a secret called `PYPI_TOKEN` with your password for your PyPI account.
      Don't worry, no one will see this password because it will be encrypted.
    - Next time you push to the branch `main` after using `bump2version`, GitHub
      actions will build and deploy your Python package to PyPI.

You can delete this entire "Setting up the Repo" section once done!

## Installation

**Stable Release:** `pip install swagit-dataset-generator`<br>
**Development Head:** `pip install git+https://github.com/evamaxfield/swagit-dataset-generator.git`

## Quickstart

```python
from swagit_dataset_generator import SwagitScraper
import dask.dataframe as dd

scraper = SwagitScraper(start_index=10000, end_index=10100, batch_size=10)
chunk_dir = scraper.run()

results_df = dd.read_parquet(f"{chunk_dir}/*")
print(results_df.meeting_body.unique().compute())
```

## Documentation

For full package documentation please visit [evamaxfield.github.io/swagit-dataset-generator](https://evamaxfield.github.io/swagit-dataset-generator).

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
