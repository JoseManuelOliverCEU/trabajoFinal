import pytest
from app.validators import clean_team_payload

def test_clean_team_payload_ok():
    d = clean_team_payload({
        "name": "  Arsenal ",
        "city": " London ",
        "stadium": " Emirates ",
        "founded_year": "1886"
    })
    assert d["name"] == "Arsenal"
    assert d["city"] == "London"
    assert d["stadium"] == "Emirates"
    assert d["founded_year"] == 1886

def test_clean_team_payload_name_required():
    with pytest.raises(ValueError) as e:
        clean_team_payload({"name": "   "})
    assert "name is required" in str(e.value)