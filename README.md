# food-inspection-monitoring
Python scripts to monitor different aspects of food inspections. This project was developed for the "Amt für Lebensmittelsicherheit und Veterinärwesen" of the canton of Fribourg. The analysis scripts expect your data to be in a certain format. You can find the exact format specification in the readme of the folder /data.


## Setup
Make sure that you have the python version specified in `.python-version` installed. We recommend using (pyenv)[https://github.com/pyenv/pyenv] for handling different Python versions.

Next, create a virtual environment in the subfolder `.venv` as follows:
`python -m venv .venv`

Activate the virtual environment:
`source .venv/bin/activate`

Install setuptools (needed to then install the package):
`pip install setuptools`

Install the package:
`pip install .`

### Developer Setup
If you want to make changes to the code, you need some additional packages.
Run:
`pip install -r requirements-dev.txt`

Then install the pre-commit hooks:
`pre-commit install`


## Usage
Once installed, you can use the package by running:
`food-inspection-monitoring --output-dir some_output_directory`

Make sure that you have the virtual environment activated.
