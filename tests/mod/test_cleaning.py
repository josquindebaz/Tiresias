from mod.cleaning import list_files


def test_list_files():
    test_path = "../utils/testing_list_files"

    """renders an empty list when no files"""
    assert list_files(test_path+"empty_dir") == []

    """find only first level directory test files"""
    expected_list = ['../utils/testing_list_files/3.TXT',
                     '../utils/testing_list_files/1.txt']
    assert list_files(test_path, recursive=False) == expected_list

    """find all text files when recursive"""
    expected_list = ['../utils/testing_list_files/3.TXT',
                     '../utils/testing_list_files/1.txt',
                     '../utils/testing_list_files/second_level/2.txt']
    actual_list = list_files(test_path)
    difference = set(actual_list) ^ set(expected_list)
    assert not difference




