# Supervisor Checklist
This template contains the basic structure of a repository needed for starting a Python project.

To adjust the template to suit your needs the best, several settings need to be adjusted:
- [ ] README.md: replace the git clone link in line 22
- [ ] rename the directory `python-project-template` to the name of your project (this is where all of your modules will be stored)
- [ ] python-project-template/__init__.py: update the information
- [ ] .gitignore: replace `python-project-template/` with the name of your project
- [ ] pyproject.toml: replace `python-project-template` with the name of your project
- [ ] pyproject.toml: replace description, author names, keywords
- [ ] pyproject.toml: replace links in [project.urls]
- [ ] docs/conf.py: replace `python-project-template/` with the name of your project
- [ ] docs/conf.py: replace the copyright and author name
- [ ] docs/index.rst: replace replace `python-project-template/` with the name of your project
- [ ] docs/Getting Started.rst: replace the content (can be done later)

The README.md file is written mainly for developers and will need to be adjusted once the project is deployed to fit user perspective better (i.e., to give more information about what the project is rathen than how to contribute to it).

## Packaging and Deployment
In order to be able to send your project over to PyPI (or TestPyPI), you will need to generate an API token and **set the variable `CI_PYPI_TOKEN` correctly** by following these steps:
1. Login to PyPI or TestPyPI
2. Go to `Account Configuration` -> `API Token` and click on `Add an API Token`
3. Copy the generated token (you will **not** be able to do this later)
4. Go to your project on GitLab, open `Settings` -> `CI/CD` and scroll down to `Variables`
5. Click on `Add variable`
6. Under key, paste `CI_PYPI_TOKEN`; under Value, paste the API token you have copied

The `CI_PYPI_TOKEN` is referenced in the `pyproject.toml` file for authentification purposes.