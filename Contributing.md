# Contributing

If you find bugs, errors, omissions, or other things that need improvement, please create an issue or a pull request at 
[https://github.com/1kastner/conflowgen/](https://github.com/1kastner/conflowgen/).
Contributions are always welcome!
We would love to see ConFlowGen grow in different dimensions, including (but not limited to) the...
- ...addition of reliable data sources for the default distributions and domain constants.
- ...improvement of the data generation process to be closer to production data
  (as long as the number of assumptions stays reasonable).
- ...more insightful previews and analyses.
- ...reduction of technical debt - some features were implemented as they were needed and better programming and software architecture patterns exist.

## Isolating the development environment

When you work on different tasks related to ConFlowGen, it is suggested to isolate the development environment from the
other Python environment(s) you use for daily tasks.
This can be achieved, e.g., with
[virtualenv](https://virtualenv.pypa.io/en/latest/)
or
[conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

## Development installation

For the development installation, instead of simply invoking `pip install` in the CLI in the project root folder, we 
additionally add the optional dependencies `dev`.
Furthermore, an additional dependency on
[pandoc](https://pandoc.org/installing.html)
exists.
The dependencies listed in `dev` allow us to run the unit tests and create the documentation.

```bash
git clone https://github.com/1kastner/conflowgen
cd conflowgen
pip install -e .[dev]
```

After modification, you can run `run_ci_light.bat` on Windows.
It executes most of the continuous integration (CI) checks
that are also automatically executed for GitHub pull requests.
On GitHub, these are implemented as GitHub workflows.
Once all jobs finish successfully,
you can create a pull request if you would like to share your changes with the ConFlowGen community.
Contributions are always welcome!
You can also run the checks individually which is explained in the following.

## Run all tests

Set up your IDE to use `pytest` in the `tests` subdirectory (relative to the module root directory).
If you use an editor without test support, you can run `python -m pytest ./tests` in the module root directory as well.
Parallel test execution has not been tested and might not work.
If you prefer to also check the test coverage, you can run
`pytest --cov="./conflowgen" --cov-report html`
from the project root directory.
After the execution, the test coverage report is located in `<project-root>/htmlcov/index.html`.
Each new feature should be covered by tests unless there are very good reasons why this is not fruitful.

## Generate the documentation

For generating the documentation, 
[sphinx](https://www.sphinx-doc.org/)
is used and mostly the default settings are maintained.

To generate the documentation, change your working directory to `<project-root>/docs`.
First, please make sure that you have up-to-date prepared sqlite databases in 
`<project-root>/docs/notebooks/data/prepared_dbs/`.
The sqlite databases compatible with the latest version of ConFlowGen are available at
https://media.tuhh.de/mls/software/conflowgen/docs/data/prepared_dbs/.
In `<project-root>/docs/download_prepared_sqlite_databases.ps1`, you find the instructions for how to download the latest databases
and where to store them.
In case you have updated the sqlite scheme, you might need to create these databases on your own with your latest
adaptions.
This is achieved by running the scripts stored in
`<project-root>/examples/Python_Script/`
and copy the resulting sqlite database into
`<project-root>/docs/notebooks/data/prepared_dbs/`.

Once the prepared databases are in place, the documentation can be built.
The documentation generation process is based on the sphinx boilerplate and the `make` process is unchanged.
For more information on that, see the
[Sphinx documentation on the build process](https://www.sphinx-doc.org/en/master/usage/quickstart.html#running-the-build).
As a Windows user, you run `.\make.bat html` from the PowerShell or CMD inside the directory `<project-root>/docs`.
Linux users invoke `make html` instead.
The landing page of the documentation is created at `<project-root>/docs/_build/html/index.html`.
It is advised to use a strict approach by using the additional argument `SPHINXOPTS="-W --keep-going`
(see the corresponding
[GitHub CI pipeline](https://github.com/1kastner/conflowgen/blob/main/.github/workflows/docs.yaml)
for reference).
The invocation should be equivalent to `python -m sphinx -W --keep-going ./docs ./docs/_build`.

## Checking the code quality

For checking the code quality, pylint, flake8, and flake8_nb are used.
Pylint is run by executing `pylint conflowgen` and `pylint setup.py` on the project root level.
For flake8, simply invoke `flake8` at the same level.
Likewise, `ruff check` lints the whole project, including the Jupyter notebooks.

## Tracking dependencies

For the installation process (both normal users and devs),
dependencies should be restricted to version ranges as little as possible.
The users and developers are expected to have an up-to-date Python environment,
e.g., by means of an isolated environment.
However, in case a future update of a dependency does break ConFlowGen,
we need to be able to return to a working state.
Thus, the library versions that are known to work are recorded and updated in a certain interval.
The requirements file is kept in the folder `.working-library-versions`.
It is generated by the invocation of the following command:
`pip freeze --local | Select-String -Pattern '^(?!-e git*).*' > .working-library-versions/requirements.txt`.
This way, past setups can be recreated in the future.

## Publishing the packages

The project is published at the following places:
- [PyPI](https://pypi.org/project/conflowgen/)
- [conda-forge](https://github.com/conda-forge/conflowgen-feedstock)
- [GitHub](https://github.com/1kastner/conflowgen/releases)
- [zenodo](https://zenodo.org/record/6280381)

While PyPI and conda packages are both based on a locally built package that is uploaded, GitHub and zenodo use git
tags to trigger the publishing process.
For all pipelines, the default settings are used.
For packing the PyPI package,
[prepare_publish.bat](https://github.com/1kastner/conflowgen/blob/main/prepare_publish.bat)
can be of guidance for Windows users.
The conda recipe is based on the PyPI package and is located at
[conflowgen-feedstock](https://github.com/conda-forge/conflowgen-feedstock).
The version number is bumped manually by updating the version number at the following places:
- [./conflowgen/metadata.py](https://github.com/1kastner/conflowgen/blob/main/conflowgen/metadata.py):
  Updates the version number for the PyPI package. Afterwards the PyPI package can be uploaded.
- The conda recipe requires a separate manual version number update in the
  [recipe](https://github.com/conda-forge/conflowgen-feedstock/blob/main/recipe/meta.yaml).
- [./CITATION.cff](https://github.com/1kastner/conflowgen/blob/main/CITATION.cff):
  Updates the version number for zenodo.
- The version number of
  [the GitHub release](https://github.com/1kastner/conflowgen/releases/new)
  is derived from the user input and can be handled after the other steps are finished.
