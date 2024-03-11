import glob
import os


def free_directory(directory):
    for file_path in glob.glob(os.path.join(directory, '*')):
        if os.path.splitext(file_path)[1] in ['.ctx', '.CTX', '.Ctx', '.txt', '.TXT', '.Txt']:
            os.remove(file_path)
