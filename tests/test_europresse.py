from mod.europresse import format_support, name_file


def test_format_support():
    support_with_parenthesis = "Le Monde (site web)"
    assert format_support(support_with_parenthesis) == "Le Monde"

    support_with_comma = "Le Point.fr, no. 202202"
    assert format_support(support_with_comma) == "Le Point.fr"

    support_with_tag = "Ouest-France                <br />Vannes ; Auray ; Ploërmel"
    assert format_support(support_with_tag) == "Ouest-France"


def test_name_file():
    date = "31/10/2023"
    prefix = "MON"
    destination = "C:/corpus/test"

    result = name_file(date, prefix, destination)

    assert result == "MON20231031A"
