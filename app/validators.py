def clean_team_payload(data: dict) -> dict:
    name = (data.get("name") or "").strip()
    if not name:
        raise ValueError("name is required")

    city = (data.get("city") or "").strip() or None
    stadium = (data.get("stadium") or "").strip() or None

    founded_year = data.get("founded_year") or None
    if founded_year is not None:
        founded_year = int(founded_year)

    return {
        "name": name,
        "city": city,
        "stadium": stadium,
        "founded_year": founded_year,
    }