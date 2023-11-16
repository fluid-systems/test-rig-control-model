# Overview

[[_TOC_]]

## Prerequisities
### Install git
Install git on your operating system following [these instructions](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Install VS Code
[Install VS Code](https://code.visualstudio.com/) on the operating system of your choice.

After the installation is finished, you can install extensions of your choice. This project contains extension recommendations in the `.vscode/extensions.json` file.

Note that there are hundreds of other extensions that can support you in various tasks - it is worth looking for tips and tricks online. We leave this up to you and name only the most basic ones for the start.

## Getting Started
### Clone this repository wherever you want to have it
Access the folder/directory of your choice and clone (make a local copy) of this repository on your machine by running

:warning: ADJUST THIS LINK
```bash
git clone https://git.rwth-aachen.de/fst-tuda/projects/project-name.git
```

If the authentication fails, you might need to add the ssh key beforehands - this will be the case if you want to access GitLab from a new machine.


### Create a virtual environment to get the required packages
#### Microsoft Windows
On Windows, run

```cmd
py -m venv env
```
The second argument is the location to create the virtual environment. Generally, you can just create this in your project and call it env.

venv will create a virtual Python installation in the env folder.

Before you can start installing or using packages in your virtual environment you’ll need to activate it. Activating a virtual environment will put the virtual environment-specific python and pip executables into your shell’s PATH.

```cmd
.\env\Scripts\activate
```

You can confirm you’re in the virtual environment by checking the location of your Python interpreter:

```cmd
where python
```
Tell pip to install all of the packages in the `requirements.txt` file using the -r flag:

```cmd
py -m pip install -r requirements.txt
```

Update the `requirements.txt` file when you install new packages.

For more detailed instructions, check https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/.
#### GNU/Linux and Apple macOS
On Linux distributions (Ubuntu, Raspberry Pi OS, etc.), run

```cmd
python3 -m venv env
```
To create the virtual environment.

```cmd
source ./env/bin/activate
```
To activate a virtual environment.

```cmd
which python3
```
To check the location of your Python interpreter.

```cmd
python3 -m pip install -r requirements.txt
```
To install the packages in the `requirements.txt`.

### Code Structure
The source code (all modules that contain your classes and functions) is located in the directory `python-project-template` (the name of this project), i.e. we are following a flat layout (see https://ta_alex.pages.rwth-aachen.de/action-items/action-items/55_software_packaging_python/#project-setup). This directory is tracked by git.

For using the source code, it is recommended to reate a script in the root directory, for example `main.py` or a Jupyter notebook, e.g. `analysis.ipynb`. This script will in most cases not have to be tracked.

### Generating documentation
This project contains documentation that can be built using Sphinx. The `.rst` files in the `docs` directory contain developer-defined documentation. The `index.rst` file is the landing page that contains the table of contents. More `.rst` files can be added to explain the code structure, logic or give a minimal example.

The `conf.py` file contains settings used by Sphinx. Among other things, it contains settings to automatically generate API documentation from in-code docstrings.

You can generate the html files by executing the following command from within the pip env:

```cmd
cd docs
make html
```
The html documentation can be viewed in your browser by opening `docs/_build/html/index.html`.

# Writing Good Code

## Language Rules

### Linting
This project uses the `flake8` linter. Linting is a static code analysis for finding programming errors, bugs, stylistic errors and suspicious constructs that do not conform with a standard - in case of flake8, with the standard [PEP8](https://peps.python.org/pep-0008/).

`flake8` will inform you about pep8 errors upon saving directly in the editor by underlining the relevant parts of code.

### Autoformatting
This project uses the `black` autoformatter and formats your code on save. Autoformatted code will look the same regardless of who wrote it and regardless of the project, so that you can focus more on the content.


## Style Rules
### Documentation
Documentation is an essential part of writing code.

:warning: All public functions, methods, classes and modules must be properly documented with docstrings.

To generate a docstring, right-click on a class, function, method or module and click on `Generate Docstring`.
This will generate a `google`-style docstring template that you have to fill out. An example for a good docstring:

```python
def find_largest_distance(point, polygon):
    """Finds the largest distance between a point and the edges of a polygon.

    Args:
        point (shapely.geometry.Point): shapely point object
        polygon (shapely.geometry.Polygon): shapely polygon object

    Returns:
        float: the largest distance between a point and the edges of a polygon
    """
    distance_list = np.array([])
    for poly_point in list(zip(*polygon.exterior.coords.xy)):
        distance = point.distance(Point(poly_point))
        distance_list = np.append(distance_list, distance)
    max_distance = max(distance_list)
    return max_distance
```
because:
- [x] short and easy to understand description
- [x] starts with a verb in third person
- [x] `type` of the args are given
- [x] args and returns are described sufficiently

Where necessary, add additional information using comments.

### Naming Convention
Follow [Guido](https://en.wikipedia.org/wiki/Guido_van_Rossum)'s recommendations (taken from [Google Python Styleguide](https://google.github.io/styleguide/pyguide.html#3164-guidelines-derived-from-guidos-recommendations)):

<table rules="all" border="1" summary="Guidelines from Guido's Recommendations"
       cellspacing="2" cellpadding="2">

  <tr>
    <th>Type</th>
    <th>Public</th>
    <th>Internal</th>
  </tr>

  <tr>
    <td>Packages</td>
    <td><code>lower_with_under</code></td>
    <td></td>
  </tr>

  <tr>
    <td>Modules</td>
    <td><code>lower_with_under</code></td>
    <td><code>_lower_with_under</code></td>
  </tr>

  <tr>
    <td>Classes</td>
    <td><code>CapWords</code></td>
    <td><code>_CapWords</code></td>
  </tr>

  <tr>
    <td>Exceptions</td>
    <td><code>CapWords</code></td>
    <td></td>
  </tr>

  <tr>
    <td>Functions</td>
    <td><code>lower_with_under()</code></td>
    <td><code>_lower_with_under()</code></td>
  </tr>

  <tr>
    <td>Global/Class Constants</td>
    <td><code>CAPS_WITH_UNDER</code></td>
    <td><code>_CAPS_WITH_UNDER</code></td>
  </tr>

  <tr>
    <td>Global/Class Variables</td>
    <td><code>lower_with_under</code></td>
    <td><code>_lower_with_under</code></td>
  </tr>

  <tr>
    <td>Instance Variables</td>
    <td><code>lower_with_under</code></td>
    <td><code>_lower_with_under</code> (protected)</td>
  </tr>

  <tr>
    <td>Method Names</td>
    <td><code>lower_with_under()</code></td>
    <td><code>_lower_with_under()</code> (protected)</td>
  </tr>

  <tr>
    <td>Function/Method Parameters</td>
    <td><code>lower_with_under</code></td>
    <td></td>
  </tr>

  <tr>
    <td>Local Variables</td>
    <td><code>lower_with_under</code></td>
    <td></td>
  </tr>

</table>

For better readability, use meaningful, expressive names instead of hard-to-understand short names. Don’t drop letters from your source code. Although dropped letters in names like `memcpy` (memory copy) and `strcmp` (string compare) were popular in the C programming language before the 1990s, they’re an unreadable style of naming that you shouldn’t use today. If a name isn’t easily pronounceable, it isn’t easily understood.

Additionally, feel free to use short phrases that can make your code read like plain English. For example, `number_of_trials` is more readable than simply `number_trials`.

[More on naming.](https://inventwithpython.com/beyond/chapter4.html)

Use a spell checker.

### Code Structure
The maximum line length is 120 characters.

Whitespaces should be automatically deleted; the autoformatter should take care of this.

Improve readability by limiting the number of nested statements.

Preferrably write short functions, and [pure functions](https://realpython.com/python-functional-programming/#:~:text=A%20pure%20function%20is%20a,to%20state%20or%20mutable%20data.) that can be tested.


### Packaging and Deployment
Check the [Packaging Flow](https://packaging.python.org/en/latest/flow/) for thorough and up-to-date information about packaging.

Update the `pyproject.toml` file by filling out the correct metadata, project names, dependencies and paths to modules.

If you have used a project structure with a `src` folder, you will need to replace the `"."` by `"src"` in `[tool.setuptools.packages.find]`.

To try out packaging before deploying a version you can be proud of into the world, use the test instance, TestPyPI (as stated in the packaging flow). The adjustment to PyPI is minor.
