import os
import shutil

from mod.cleaning import list_files


def test_list_files():
    create_filesystem()

    assert list_files("up_dir/empty_directory") == []
    without_recursion = list_files("up_dir", recursive=False)
    assert set(without_recursion) == set(['up_dir/b.txt', 'up_dir/a.txt'])
    with_recursion = list_files("up_dir", recursive=True)
    expected = ['up_dir/b.txt', 'up_dir/a.txt', 'up_dir/sub_dir/d.txt', 'up_dir/sub_dir/c.txt']
    assert set(with_recursion) == set(expected)

    delete_filesystem()


def create_filesystem():
    delete_filesystem()

    os.makedirs('up_dir/sub_dir')
    os.mkdir("up_dir/empty_directory")

    open('up_dir/a.txt', 'a').close()
    open('up_dir/b.txt', 'a').close()
    open('up_dir/sub_dir/c.txt', 'a').close()
    open('up_dir/sub_dir/d.txt', 'a').close()


def delete_filesystem():
    if not os.path.isdir("up_dir"):
        return 0

    shutil.rmtree("up_dir")
