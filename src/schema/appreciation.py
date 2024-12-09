import pathlib

APPRECIATION_PATH = pathlib.Path("data", "appreciation.xlsx")


class Appreciation:
    """Schema of inspection appreciation data."""

    id_dossier = "ID_Dossier"
    danger_level = "Niveaux_Danger"
