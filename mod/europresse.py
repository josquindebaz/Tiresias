import glob
import re
import html
import os
import datetime

try:
    from cleaning import Cleaner
    from supports import Publi
except ModuleNotFoundError:
    from mod.cleaning import Cleaner
    from mod.supports import Publi


def format_support(support):
    motif = re.compile(r'\s*([<(,]).*$')
    return motif.sub('', support)


def strip_tags(text):
    motif = re.compile(r'(<(\S+) class=(.))')

    if not motif.search(text):
        return text

    while motif.search(text):
        catches = motif.split(text, 1)
        fragment_to_keep = re.split('%s>' % catches[3], catches[4], 1)[1]
        fragment_to_keep = re.sub('</%s>' % catches[2], '', fragment_to_keep, 1)
        text = catches[0] + fragment_to_keep

    return re.sub('</*mark>', '', text)


def get_date(given_date):

    months = {
        "janvier": "01",
        'février': "02",
        "mars": "03",
        "avril": "04",
        "mai": "05",
        "juin": "06",
        "juillet": "07",
        "août": "08",
        "septembre": "09",
        "octobre": "10",
        "novembre": "11",
        "décembre": "12",
        "January": "01",
        'February': "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12"
    }

    day_first_date = re.compile(r"(\d+) (\S*) (\d{4})")
    month_first_date = re.compile(r"(\S*)\s+(\d+)[,\s]{2,}(\d{4})")

    if not day_first_date.search(given_date) and not month_first_date.search(given_date):
        print("Problem reading date [%s]" % given_date)
        return False

    if day_first_date.search(given_date):
        day, month, year = day_first_date.search(given_date).group(1, 2, 3)
        if month not in months:
            print("I don't know this month %s" % month)
            return False
    elif month_first_date.search(given_date):
        month, day, year = month_first_date.search(given_date).group(1, 2, 3)
        if month not in months:
            print("I don't know this month: %s" % month)
            return False

    return "%s/%s/%s" % ("%02d" % int(day), months[month], year)


def in_tag(html_source, tag):
    motif = re.compile(r'(<(\S*) \S*=[\'"]%s[\'"][^>]*>)' % tag)

    if not motif.search(html_source):
        # print("Can't find tag %s" % tag)
        return False

    elements = motif.split(html_source)
    if len(elements) != 4:
        print("problem with element list size")
        return False

    closing = re.split("</%s>" % elements[2], elements[3], 1)
    if len(closing) != 2:
        print("Can't find closing %s" % elements[2])
        return False

    return closing[0].strip()


def parse_article(article_content):
    if re.search('<p class="link-not-hosted">', article_content):
        print("only a link")
        return False
    elif re.search('class="DocPublicationName">(Rapports|Reports) -', article_content):
        print("only a report extract")
        return False
    elif re.search('<div class="twitter">', article_content):
        print("only a tweet")
        return False

    article_content = html.unescape(article_content)
    # print("split header and content")
    header, content = re.split('</header>', article_content)

    # print("get header infos")
    publication_name = in_tag(header, "DocPublicationName")
    publication_name = format_support(publication_name)
    # print("publication_name")
    date = in_tag(header, "DocHeader")
    date = get_date(date)
    # print("date %s" %date)
    title = in_tag(header, "titreArticle")
    title = strip_tags(title)
    narrator = in_tag(header, "docAuthors")
    m_subtitle = re.compile("<b><p>(.*)</p></b>")
    if m_subtitle.search(header):
        subtitle = m_subtitle.search(header).group(1)
    else:
        subtitle = False

    text = in_tag(article_content, "docOcurrContainer")
    text = strip_tags(text)

    return {
        "source": publication_name,
        "date": date,
        "title": title,
        "narrator": narrator,
        "subtitle": subtitle,
        "text": text
    }


def europresse_file_parser(filepath):
    with open(filepath, 'rb') as file_pointer:
        buffer = file_pointer.read().decode('utf-8')
    articles = re.split('<article>', buffer)[1:]
    parsed_articles = []

    for article in articles:
        parsed = parse_article(article)
        if parsed:
            parsed_articles.append(parsed)

    return articles, parsed_articles


def name_file(date, prefix, destination):
    index, base = "A", 64
    date = "".join(reversed(date.split("/")))
    name = "%s%s%s" % (prefix, date, index)
    path = os.path.join(destination, name + ".txt")

    while os.path.isfile(path):
        if ord(index[-1]) < 90:
            index = chr(ord(index[-1]) + 1)
        else:
            base += 1
            index = "A"
        if base > 64:  # if Z => 2 letters
            index = chr(base) + index
        name = "%s%s%s" % (prefix, date, index)
        path = os.path.join(destination, name + ".txt")

    return name


def get_support_values(article):
    supports = Publi()
    if article['source'] not in supports.codex.keys():
        return "EUROPRESSE", article['source'], "unknown source"

    return (supports.codex[article['source']]['abr'],
            supports.codex[article['source']]['source'],
            supports.codex[article['source']]['type'])


def build_file_contents(article, cleaning, source, source_type):
    text = article['title'] + "\r\n.\r\n"
    text += article['subtitle'] + "\r\n.\r\n" if article['subtitle'] else ""
    text += article['text']

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
        "Processed by Tiresias on %s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "",
        "n",
        "n",
        ""
    ]
    ctx = "\r\n".join(ctx)

    if cleaning:
        txt_cleaner = Cleaner(text.encode('utf-8'))
        text = txt_cleaner.content
        ctx_cleaner = Cleaner(ctx.encode('utf-8'))
        ctx = ctx_cleaner.content

    return ctx, text


def write_files(filename, ctx, text, destination):
    # to bytes
    ctx = ctx.encode('latin-1', 'xmlcharrefreplace')
    text = text.encode('latin-1', 'xmlcharrefreplace')

    path = os.path.join(destination, filename + ".txt")
    with open(path, 'wb') as f:
        f.write(text)
    path = os.path.join(destination, filename + ".ctx")
    with open(path, 'wb') as f:
        f.write(ctx)


class EuropresseProsperoFileBuilder(object):
    def __init__(self, article, destination, cleaning=True):
        prefix, source, source_type = get_support_values(article)

        self.filename = name_file(article['date'], prefix, destination)

        ctx, txt = build_file_contents(article, cleaning, source, source_type)

        write_files(self.filename, ctx, txt, destination)


def free_test_directory(directory):
    for file_path in glob.glob(os.path.join(directory, '*')):
        if os.path.splitext(file_path)[1] in ['.ctx', '.CTX', '.Ctx', '.txt', '.TXT', '.Txt']:
            os.remove(file_path)


if __name__ == "__main__":
    directory_path = "../tests/mod/europresse/"
    free_test_directory(directory_path)

    europresse_files = glob.glob(os.path.join(directory_path, "*.HTM*"))
    print("# Found %d Europresse file(s)" % len(europresse_files))

    for filepath in europresse_files:
        print("# Parsing %s" % filepath)
        articles, parsed_articles = europresse_file_parser(filepath)
        print("## Found %d article(s)" % len(articles))
        print("## Parsed %d article(s)" % len(parsed_articles))

    for article in parsed_articles:
        EuropresseProsperoFileBuilder(article, directory_path)

    free_test_directory(directory_path)
