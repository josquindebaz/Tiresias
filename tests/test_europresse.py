import filecmp
import glob
import os

from mod.europresse import format_support_name, ParseHtml, ProcessArticle, strip_tags_with_class, fetch_date


def test_europresse_e2e():
    current_directory = os.getcwd()
    if os.path.basename(current_directory) == "tests":
        directory_path = "."
    else:
        directory_path = "tests"

    free_directory(directory_path)

    to_parse = os.path.join(directory_path, "europresse/pesquet_19-11-21_a_26-10-23.HTML")
    parser = ParseHtml(to_parse)
    assert len(parser.articles) == 305
    assert len(parser.parsed_articles) == 292

    ProcessArticle(parser.parsed_articles[0], directory_path)

    txt_to_compare = os.path.join(directory_path, "europresse/EUROPRESSE20231023A.txt")
    with open(txt_to_compare, "r", encoding='cp1252') as expected:
        expected_txt = expected.read()
    txt_generated = os.path.join(directory_path, "EUROPRESSE20231023A.txt")
    with open(txt_generated, "r", encoding='cp1252') as result:
        generated_txt = result.read()

    assert expected_txt == generated_txt

    ctx_to_compare = os.path.join(directory_path, "europresse/EUROPRESSE20231023A.ctx")
    with open(ctx_to_compare, "r", encoding='cp1252') as expected:
        expected_lines = expected.readlines()
    ctx_generated = os.path.join(directory_path, "EUROPRESSE20231023A.ctx")
    with open(ctx_generated, "r", encoding='cp1252') as result:
        result_lines = result.readlines()
        print(result_lines)

    assert expected_lines[0:10] == result_lines[0:10]

    free_directory(directory_path)


def test_format_support_name():
    support_with_parenthesis = "Le Monde (site web)"
    assert format_support_name(support_with_parenthesis) == "Le Monde"

    support_with_comma = "Le Point.fr, no. 202202"
    assert format_support_name(support_with_comma) == "Le Point.fr"

    support_with_tag = "Ouest-France                <br />Vannes ; Auray ; Ploërmel"
    assert format_support_name(support_with_tag) == "Ouest-France"


def free_directory(directory):
    for file_path in glob.glob(os.path.join(directory, '*')):
        if os.path.splitext(file_path)[1] in ['.ctx', '.CTX', '.Ctx', '.txt', '.TXT', '.Txt']:
            os.remove(file_path)


def test_strip_tags_with_class():
    result = strip_tags_with_class("<foo class='bar'>something</foo>")
    assert result == "something"


def test_fetch_date():
    result = fetch_date("lundi 16 octobre 2023 - 16:55:20 -0000 1017 mots")
    assert result == "16/10/2023"

