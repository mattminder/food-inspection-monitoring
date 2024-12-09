# food-inspection-monitoring
Python scripts to monitor different aspects of food inspections. This project was developed for the "Amt für Lebensmittelsicherheit und Veterinärwesen" of the canton of Fribourg. The analysis scripts expect your data to be in a certain format. You can find the exact format specification in the readme of the folder /data.


## Setup
Make sure that you have the python version specified in `.python-version` installed. We recommend using (pyenv)[https://github.com/pyenv/pyenv] for handling different Python versions.

Next, create a virtual environment in the subfolder `.venv` as follows:
`python -m venv .venv`

Activate the virtual environment:
`source .venv/bin/activate`

Install all necessary packages:
`pip install -r requirements.txt`
