import functools
import pandas as pd

from src.schema.inspection import Inspection
from src.schema.activity import Activity


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


def _merge_inspection_and_activities(inspections, food_activities):
    # TODO: Make sure inspections are complete
    # TODO: Make sure that activities have base frequency > 0 and that they are active

    _merged = inspections.merge(
        food_activities.drop(
            ["ID_Entreprise", "Canton", "Domaine_Activite", "Insp_Contr"], axis=1
        ),
        left_on=Inspection.activity_uid,
        right_on=Activity.activity_uid,
        how="left",
    )
    # TODO: Change this to inner?
