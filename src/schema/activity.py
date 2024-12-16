import pathlib
import enum

ACTIVITY_PATH = pathlib.Path("data", "activity.xlsx")


class Activity:
    """Schema of activity table."""

    base_frequency = "Frequence_Base"
    business_id = "ID_Entreprise"
    activity_domain = "Domaine_Activite"
    canton = "Canton"
    last_risk_factor = "Last_INSP_Facteur"
    status = "Statut_Categorie"


class ActivityDomain(enum.Enum):
    FOOD = "Denrées alimentaires/Objets usuels"


class ActivityStatus(enum.Enum):
    ACTIVE = "Aktiv"
