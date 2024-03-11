import glob
import os

from mod.factiva import ParseHtm
from tests.utils import free_directory


def test_can_parse_htm():
    current_directory = os.getcwd()
    if os.path.basename(current_directory) == "tests":
        directory_path = "."
        support_path = "../data/support.publi"
    else:
        directory_path = "tests"
        support_path = "data/support.publi"

    free_directory(directory_path)

    to_parse = os.path.join(directory_path, "factiva/Factiva.htm")
    parser = ParseHtm(to_parse)

    assert len(parser.content) == 40

    parser.get_supports(support_path)

    assert len(parser.unknowns) == 0

    free_directory("temp")
    parser.write_prospero_files("temp")

    txt_generated = glob.glob("temp/*.txt")
    assert len(txt_generated) == 40

    ctx_generated = glob.glob("temp/*.ctx")
    assert len(ctx_generated) == 40

    free_directory("temp")
