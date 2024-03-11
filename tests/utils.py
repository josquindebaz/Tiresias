import glob
import os
import shutil


def free_directory(directory):
    for file_path in glob.glob(os.path.join(directory, '*')):
        if os.path.splitext(file_path)[1] in ['.ctx', '.CTX', '.Ctx', '.txt', '.TXT', '.Txt']:
            os.remove(file_path)


def delete_directory(directory):
    if not os.path.isdir(directory):
        return 0

    shutil.rmtree(directory)
