import os
from datetime import datetime
from mod.cleaning import Cleaner


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


def write_file(destination, filename, extension, content):
    path = os.path.join(destination, filename + extension)
    encoded_content = content.encode('latin-1', 'xmlcharrefreplace')
    with open(path, 'wb') as f:
        f.write(encoded_content)


def create_ctx_content(article, source, source_type):
    ctx = [
        "fileCtx0005",
        article['title'],
        source,
        "",
        "",
        article['date'],
        source,
        source_type,
        "",
        "",
        "",
        "Processed by Tiresias on %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "",
        "n",
        "n",
        ""
    ]
    ctx = "\r\n".join(ctx)
    return ctx


def clean_content(cleaning_required, ctx_content, txt_content):
    if not cleaning_required:
        return ctx_content, txt_content

    txt_cleaner = Cleaner(txt_content.encode('utf-8'))
    ctx_cleaner = Cleaner(ctx_content.encode('utf-8'))

    return ctx_cleaner.content, txt_cleaner.content
