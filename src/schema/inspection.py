import pathlib
import enum
from src.schema.activity import Activity

INSPECTION_PATH = pathlib.Path("data", "inspection.xlsx")


class Inspection:
    """Schema of inspection table."""

    id_dossier = "ID_Dossier"
    type_dossier = "Type_Dossier"
    activity_domain = Activity.activity_domain
    date = "Date_Inspection"
    activity_uid = Activity.activity_uid


class InspectionDossierType(enum.Enum):
    SAMPLING_EXTRACTION = "Pbnahme"
