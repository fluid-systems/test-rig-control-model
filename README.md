# Overview

This repository contains the code for the paper "Applying the Elastic Water Column Model with Dynamic Elements to a Physical Test Rig" by Kevin T. Logan, Michaela Lestakova and Peter F. Pelz, presented at the WDSA/CCWI 2026.

<details> <summary> paper abstract </summary>
Applying control methods to water distribution systems requires suitable system models.
The elastic water column model, which has been expanded to incorporate dynamic elements like pumps and valves, is a promising model for control applications due to its formulation in state-space form. However, the model has so far only been validated numerically. The presented work implements the elastic water column model with dynamic elements for water distribution systems in Python and applies it to a small-scale physical test rig. The experimental results are compared with the simulation results to show that the EWCM-DE implementation is a suitable tool for real-time control.
</details>

The implementation of the elastic water column model with dynamic elements is in the directory `test_rig_control_model`. The directory `notebooks` contains jupyter notebooks corresponding to the scenarios introduced in the aforementioned paper:


## Getting Started
### Clone this repository wherever you want to have it
Clone this repository using

:warning: ADJUST THIS LINK
```bash
git clone git@git.rwth-aachen.de:fst-tuda/projects/emergencity/resilince-demonstrator/test-rig-control-model.git
```

### Create a virtual environment to get the required packages
#### Python with Pyenv
It is quite useful to use `pyenv` as a tool for managing Python verions installed on your system. You can find instructions on how to download and install `pyenv` for [Linux/Mac](https://github.com/pyenv/pyenv) and [Windows](https://github.com/pyenv-win/pyenv-win/blob/master/docs/installation.md).
In any case, you need to ensure that the Python version specified in the project's dependencies in `pyproject.toml` (3.12.1) is available.

#### Poetry
We use `poetry` for package management and virtual environments in this project. You can find installation instructions for `poetry` [here](https://python-poetry.org/docs/#installing-with-the-official-installer).

#### Getting Started
After cloning the project, open the folder containing it in VS Code. Ensure that the required Python version is the one used by VS Code. When using `pyenv` you can do this by first checking that it is available with

```bash
pyenv versions
```

To make the specific version used in the folder, you can run

```bash
pyenv local 3.12.1
```

You need to specify two settings in `poetry` before installing dependencies and creating a virtual environment.

Set

```bash
poetry config virtualenvs.prefer-active-python true
```

This ensures that the currently active version of Python gets used for creating the environment. Not doing this will lead to conflicts between the specified dependencies and the Python version in the virtual environment `poetry` creates.

Set

```bash
poetry config virtualenvs.in-project true
```

This ensures that the virtual environment gets installed in the project folder rather than the default directory for `poetry`.

Now you can install dependencies and create the virtual environment by running

```bash
poetry install
```

Don't forget to select the Python in the created `.venv` as the executable used in VS Code for this project.

#### For further development: Pre-commit hooks, linting and autoformatting
This project uses [pre-commit](https://pre-commit.com/) hooks to ensure that all code that gets pushed to the remote repository complies with formatting and typing standards.
Install the pre-commit hooks by running
```
poetry run pre-commit install
```
On every commit, this will run linting and formatting as well as type checking. Accordingly, you need to ensure to fully type your code. Lint and format on save using `ruff` as specified in the development dependencies in the `pyproject.toml`.

## Acknowledgements
This work has been funded by the LOEWE initiative (Hesse, Germany) within the emergenCITY center [LOEWE/1/12/519/03/05.001(0016)/72].
