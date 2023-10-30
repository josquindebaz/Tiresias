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


def form_support(s):
    m = re.compile(r"\s*(<|\(|,).*$")
    n = m.sub('', s)
    return n


def strip_tags(text):
    motif = re.compile(r'(<(\S+) class=(.))')

    if not motif.search(text):
        return text

    while motif.search(text):
        catches = motif.split(text, 1)
        t = re.split("%s>" % catches[3], catches[4], 1)[1]
        t = re.sub("</%s>" % catches[2], "", t, 1)
        text = catches[0] + t
    text = re.sub("</*mark>", "", text)
    return text


def get_date(d):
    # print(d)
    m = re.compile(r"(\d+) (\S*) (\d{4})")
    m2 = re.compile(r"(\S*)\s+(\d+)[,\s]{2,}(\d{4})")
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
    if m.search(d):
        day, month, year = m.search(d).group(1, 2, 3)
        if month not in months:
            print("I don't know this month %s" % month)
            return False
        else:
            month = months[month]
        return "%s/%s/%s" % ("%02d" % int(day), month, year)
    elif m2.search(d):
        month, day, year = m2.search(d).group(1, 2, 3)
        if month not in months:
            print("I don't know this month %s" % month)
            return False
        else:
            month = months[month]
        return "%s/%s/%s" % ("%02d" % int(day), month, year)
    else:
        print("Problem reading date [%s]" % d)
        return False


def in_tag(html_source, tag):
    motif = re.compile(r'(<(\S*) \S*=[\'"]%s[\'"][^>]*>)' % tag)
    if motif.search(html_source):
        elements = motif.split(html_source)
        if len(elements) == 4:
            closing = re.split("</%s>" % elements[2], elements[3], 1)
            if len(closing) == 2:
                return closing[0].strip()
            else:
                print("Can't find closing %s" % elements[2])
                return False
        else:
            print("problem with element list size")
            return False
    else:
        # print("Can't find tag %s" % tag)
        return False


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
    else:
        article_content = html.unescape(article_content)
        # print("split header and content")
        header, content = re.split('</header>', article_content)

        # print("get header infos")
        publication_name = in_tag(header, "DocPublicationName")
        publication_name = form_support(publication_name)
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

class EuropresseArticleExtractor(object):
    def __init__(self, a, destination, c=1):
        self.destination = destination
        s = Publi()
        if a['source'] not in s.codex.keys():
            prefix = "EUROPRESSE"
            source = a['source']
            source_type = "unknown source"
        else:
            prefix = s.codex[a['source']]['abr']
            source = s.codex[a['source']]['source']
            source_type = s.codex[a['source']]['type']

        self.filename = self.file_name(a['date'], prefix)

        text = a['title'] + "\r\n.\r\n"
        text += a['subtitle'] + "\r\n.\r\n" if a['subtitle'] else ""
        text += a['text']

        ctx = [
            "fileCtx0005",
            a['title'],
            source,
            "",
            "",
            a['date'],
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

        if c:
            cl_txt = Cleaner(text.encode('utf-8'))
            text = cl_txt.content.encode('latin-1', 'xmlcharrefreplace')  # to bytes
            cl_ctx = Cleaner(ctx.encode('utf-8'))
            ctx = cl_ctx.content.encode('latin-1', 'xmlcharrefreplace')  # to bytes
        else:
            ctx = ctx.encode('latin-1', 'xmlcharrefreplace')  # to bytes
            text = text.encode('latin-1', 'xmlcharrefreplace')  # to bytes

        path = os.path.join(self.destination, self.filename + ".txt")
        with open(path, 'wb') as f:
            f.write(text)

        path = os.path.join(self.destination, self.filename + ".ctx")
        with open(path, 'wb') as f:
            f.write(ctx)

    def file_name(self, date, prefix):
        index, base = "A", 64
        date = "".join(reversed(date.split("/")))
        name = "%s%s%s" % (prefix, date, index)
        path = os.path.join(self.destination, name + ".txt")
        while os.path.isfile(path):
            if ord(index[-1]) < 90:
                index = chr(ord(index[-1]) + 1)
            else:
                base += 1
                index = "A"
            if base > 64:  # if Z => 2 letters
                index = chr(base) + index
            name = "%s%s%s" % (prefix, date, index)
            path = os.path.join(self.destination, name + ".txt")
        return name


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
        EuropresseArticleExtractor(article, directory_path)

    free_test_directory(directory_path)
