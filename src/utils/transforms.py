from src.schema.appreciation import Appreciation
from src.schema.activity import Activity


def get_inspection_completeness(insp_appreciation):
    """Takes appreciation, and calculates whether a given inspection was completed."""
    insp_completeness = (
        insp_appreciation.groupby([Appreciation.id_dossier])
        .agg({Appreciation.danger_level: lambda x: x.notna().sum()})
        .rename({Appreciation.danger_level: "Checked_Categories"}, axis=1)
        .reset_index()
    )
    completeness = insp_completeness["Checked_Categories"] == 6
    return completeness


def get_number_required_controls(food_activity, use_risk_factor):
    """Calculates number of controls needed each year, given the active business activities.

    The parameter "use_risk_factor" specifies whether to take into account the risk factor or not.
    """
    # for every business, consider only the activity that needs the most inspections
    most_relevant_activity = get_most_relevant_activity(food_activity)

    # what's a bit confusing about the naming is that the field "base_frequency" contains the period
    period = most_relevant_activity[Activity.base_frequency]

    if use_risk_factor:
        period = period * most_relevant_activity[Activity.last_risk_factor].fillna(1)

    frequency = 1 / period
    needed_inspections = frequency.groupby(
        most_relevant_activity[Activity.canton]
    ).sum()
    return needed_inspections


def get_most_relevant_activity(food_activity):
    """For every business, extracts the activity with the lowest 'Frequence Base'."""
    return (
        food_activity[
            food_activity[Activity.base_frequency].notna()
            & (food_activity[Activity.base_frequency] > 0)
        ]
        .sort_values(Activity.base_frequency)
        .groupby(Activity.business_id)
        .head(1)
    )
