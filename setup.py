import setuptools

REQUIREMENTS = [
    "pandas",
    "click",
    "numpy",
    "matplotlib",
    "openpyxl",
]

setuptools.setup(
    name="food-inspection-monitoring",
    version="0.1.0",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": "food-inspection-monitoring = src.cli.main:cli",
    },
)
