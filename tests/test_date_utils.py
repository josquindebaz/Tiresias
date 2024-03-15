from mod.date_utils import fetch_date


def test_fetch_date():
    result = fetch_date("lundi 16 octobre 2023 - 16:55:20 -0000 1017 mots")
    assert result == "16/10/2023"
