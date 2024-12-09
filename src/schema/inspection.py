import pathlib
import enum

INSPECTION_PATH = pathlib.Path("data", "inspection.xlsx")


class Inspection:
    """Schema of inspection table."""

    id_dossier = "ID_Dossier"
    type_dossier = "Type_Dossier"
    activity_domain = "Domaine_Activite"
    date = "Date_Inspection"


class InspectionDossierType(enum.Enum):
    SAMPLING_EXTRACTION = "Pbnahme"


class InspectionActivityDomain(enum.Enum):
    FOOD = "Denrées alimentaires/Objets usuels"
