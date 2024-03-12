import os


def name_file(formatted_date, prefix, destination):
    index, base = "A", 64
    formatted_date = "".join(reversed(formatted_date.split("/")))
    file_name = "%s%s%s" % (prefix, formatted_date, index)

    path = os.path.join(destination, file_name + ".txt")

    while os.path.isfile(path):
        if ord(index[-1]) < 90:
            index = chr(ord(index[-1]) + 1)
        else:
            base += 1
            index = "A"

        if base > 64:  # if index is Z => add a letter
            index = chr(base) + index

        file_name = "%s%s%s" % (prefix, formatted_date, index)
        path = os.path.join(destination, file_name + ".txt")

    return file_name
