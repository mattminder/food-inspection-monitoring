import pathlib
import click
from src.utils.loaders import (
    read_complete_food_inspections,
    read_active_relevant_food_activity,
)
from src.plots.lateness_over_time import plot_lateness_over_time


@click.command()
@click.option(
    "--output-dir",
    help="Directory into which to write the files",
    type=click.Path(
        exists=True, file_okay=False, writable=True, path_type=pathlib.Path
    ),
    required=True,
)
def cli(output_dir):
    complete_food_inspections = read_complete_food_inspections()
    food_activities = read_active_relevant_food_activity()
    plot_lateness_over_time(complete_food_inspections, food_activities, output_dir)
