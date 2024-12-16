import functools
import pandas as pd
from matplotlib import pyplot as plt

from src.schema.inspection import Inspection
from src.schema.activity import Activity
from src.plots.plot_paths import LATENESS_OVER_TIME


class _EngineeredColumns:

    next_inspection_due_date = "Next_Inspection_Due_Date"


def _calculate_percentage_late_single_canton(single_canton, start_date, end_date):
    """Calculates the percentage of overdue inspections in a single canton every month.

    At every month, we take the last known inspection. Then, we look at whether the next inspection
    would already have been due.
    """

    merged_sorted = single_canton.sort_values(Inspection.date)

    date_range = pd.date_range(start_date, end_date, freq=pd.offsets.MonthBegin(1))
    number_invalid = []

    for month in date_range:
        current_state = (
            merged_sorted[merged_sorted[Inspection.date] < month]
            .groupby(Inspection.activity_uid)
            .last()
        )
        currently_late = (
            current_state[_EngineeredColumns.next_inspection_due_date] < month
        ).mean()
        number_invalid.append(currently_late)

    return pd.Series(number_invalid, index=date_range)


def _get_start_end_date(merged):
    return (merged[Inspection.date].min(), merged[Inspection.date].max())


def _get_next_inspection(df):
    def inner(x):
        last_date = x[Inspection.date]
        frequency = x[Activity.base_frequency]

        if last_date is pd.NaT:
            return pd.NaT

        # map Februaury 29th in leap year to March 1st
        if last_date.month == 2 and last_date.day == 29 and frequency % 4 != 0:
            return pd.Timestamp(
                year=last_date.year + int(frequency),
                month=3,
                day=1,
            )

        # keep the same date, but shift the year
        return pd.Timestamp(
            year=last_date.year + int(frequency),
            month=last_date.month,
            day=last_date.day,
        )

    return df.apply(inner, axis=1)


def _calculate_number_invalid(merged):
    start_date, end_date = _get_start_end_date(merged)

    return merged.groupby(Activity.canton).apply(
        functools.partial(
            _calculate_percentage_late_single_canton,
            start_date=start_date,
            end_date=end_date,
        ),
        include_groups=False,
    )


def _join_base_frequency(complete_inspections, food_activities):
    """Joins the base frequency to the inspections."""
    return complete_inspections.merge(
        food_activities[[Activity.activity_uid, Activity.base_frequency]],
        left_on=Inspection.activity_uid,
        right_on=Activity.activity_uid,
        how="inner",
    )


def _plot(number_invalid, output_dir):
    (number_invalid * 100).T.plot(figsize=(12, 4))
    plt.xlabel("Year")
    plt.ylabel("Percentage Late")
    plt.savefig(output_dir / LATENESS_OVER_TIME)


def plot_lateness_over_time(complete_inspections, food_activities, output_dir):
    """Creates a plot of the number of late inspections over time."""
    with_base_frequency = _join_base_frequency(complete_inspections, food_activities)

    # Engineer a new column for the next inspection due date
    with_base_frequency[
        _EngineeredColumns.next_inspection_due_date
    ] = _get_next_inspection(with_base_frequency)

    # Calculate and plot the number of invalid entries
    number_invalid = _calculate_number_invalid(with_base_frequency)
    _plot(number_invalid, output_dir)
