import pandas as pd
from src.utils.transforms import get_inspection_completeness
from src.schema.appreciation import APPRECIATION_PATH
from src.schema.inspection import (
    INSPECTION_PATH,
    Inspection,
    InspectionDossierType,
)
from src.schema.activity import ACTIVITY_PATH, ActivityDomain, Activity, ActivityStatus


def read_food_inspections():
    inspections = pd.read_excel(str(INSPECTION_PATH))

    # remove pbnahme and water-related stuff
    filtered = inspections[
        (
            inspections[Inspection.type_dossier]
            != InspectionDossierType.SAMPLING_EXTRACTION
        )
        & (inspections[Inspection.activity_domain] == ActivityDomain.FOOD)
    ].copy()

    # parse date
    filtered[Inspection.date] = pd.to_datetime(
        filtered[Inspection.date],
        format="%d.%m.%Y",
    )
    return filtered


def read_inspection_appreciation():
    appreciation = pd.read_excel(str(APPRECIATION_PATH))
    return appreciation


def read_complete_food_inspections():
    inspections = read_food_inspections()
    insp_appreciation = read_inspection_appreciation()

    # get the inspection ids that are complete
    inspection_completeness = get_inspection_completeness(insp_appreciation)
    complete_inspection_ids = inspection_completeness[inspection_completeness].index

    # return entries with a complete inspection
    return inspections[inspections[Inspection.id_dossier].isin(complete_inspection_ids)]


def read_food_activity():
    activity = pd.read_excel(str(ACTIVITY_PATH))

    is_food_activity = activity[Activity.activity_domain] == ActivityDomain.FOOD
    is_active = activity[Activity.status] == ActivityStatus.ACTIVE
    return activity[is_food_activity & is_active]
