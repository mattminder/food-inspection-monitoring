from src.schema.appreciation import Appreciation


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
