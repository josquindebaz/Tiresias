import os

from mod.file_utils import name_file
from tests.utils import delete_directory


def test_file_name():
    current_directory = os.getcwd()
    if os.path.basename(current_directory) == "tests":
        directory_path = 'europresse_file_name_test'
    else:
        directory_path = os.path.join("tests/", "europresse_file_name_test")

    delete_directory(directory_path)
    os.mkdir(directory_path)

    date = '23/10/2023'
    prefix = "EUROPRESSE"

    result = name_file(date, prefix, directory_path)
    assert result == "EUROPRESSE20231023A"

    open(os.path.join(directory_path, "EUROPRESSE20231023A.txt"), 'a').close()
    result = name_file(date, prefix, directory_path)
    assert result == "EUROPRESSE20231023B"

    for letter in range(65, 91):
        open(os.path.join(directory_path, f"EUROPRESSE20231023{chr(letter)}.txt"), 'a').close()

    result = name_file(date, prefix, directory_path)
    assert result == "EUROPRESSE20231023AA"

    delete_directory(directory_path)