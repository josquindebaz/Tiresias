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


def format_support_name(support):
    motif = re.compile(r"\s*(<|\(|,).*$")
    return motif.sub('', support)


def strip_tags_with_class(text):
    motif = re.compile(r'(<(\S+) class=(.))')

    if not motif.search(text):
        return text

    while motif.search(text):
        catches = motif.split(text, 1)
        to_keep = re.split(f"{catches[3]}>", catches[4], 1)[1]
        to_keep = re.sub(f"</{catches[2]}>", "", to_keep, 1)
        text = catches[0] + to_keep

    text = re.sub("</*mark>", "", text)

    return text


def fetch_date(given_date):
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

    day_first_date_format = re.compile(r"(\d+) (\S*) (\d{4})")
    month_first_date_format = re.compile(r"(\S*)\s+(\d+)[,\s]{2,}(\d{4})")

    if not day_first_date_format.search(given_date) and not month_first_date_format.search(given_date):
        print("Problem reading date [%s]" % given_date)
        return False

    if day_first_date_format.search(given_date):
        day, month, year = day_first_date_format.search(given_date).group(1, 2, 3)
        if month not in months:
            print("I don't know this month %s" % month)
            return False

    elif month_first_date_format.search(given_date):
        month, day, year = month_first_date_format.search(given_date).group(1, 2, 3)
        if month not in months:
            print("I don't know this month %s" % month)
            return False

    return "%s/%s/%s" % (f"{int(day):02d}", months[month], year)


def in_tag(html_source, tag_class):
    motif = re.compile(r'(<(\S*) \S*=[\'"]%s[\'"][^>]*>)' % tag_class)

    if not motif.search(html_source):
        return False

    elements = motif.split(html_source)

    if not len(elements) == 4:
        # print("problem with element list size")
        return False

    tag_type = elements[2]
    after_tag = elements[3]
    closing = re.split("</%s>" % tag_type, after_tag, 1)

    if not len(closing) == 2:
        # print("Can't find closing %s" % tag_type)
        return False

    return closing[0].strip()


def parse_article(article_content):
    if re.search('<p class="link-not-hosted">', article_content):
        # print("only a link")
        return False
    elif re.search('class="DocPublicationName">(Rapports|Reports) -', article_content):
        # print("only a report extract")
        return False
    elif re.search('<div class="twitter">', article_content):
        # print("only a tweet")
        return False

    article_content = html.unescape(article_content)
    header, body = re.split('</header>', article_content)

    result = get_header_infos(header)

    text = in_tag(article_content, "docOcurrContainer")
    result["text"] = strip_tags_with_class(text)

    return result


def get_header_infos(header):
    result = {}
    publication_name = in_tag(header, "DocPublicationName")
    result["source"] = format_support_name(publication_name)

    result["date"] = fetch_date(in_tag(header, "DocHeader"))

    title = in_tag(header, "titreArticle")
    result["title"] = strip_tags_with_class(title)

    result["narrator"]  = in_tag(header, "docAuthors")

    result["subtitle"] = False
    m_subtitle = re.compile("<b><p>(.*)</p></b>")
    if m_subtitle.search(header):
        result["subtitle"] = m_subtitle.search(header).group(1)

    return result


def read_file(filename):
    with open(filename, 'rb') as file_pointer:
        buffer = file_pointer.read().decode('utf-8')
    return buffer


def separate_articles(buffer):
    return re.split('<article>', buffer)[1:]


class EuropresseHtmlParser(object):
    def __init__(self, filename):

        self.parsed_articles = []

        buffer = read_file(filename)

        self.articles = separate_articles(buffer)

        for article in self.articles:
            parsed = parse_article(article)
            if parsed:
                self.parsed_articles.append(parsed)


class ProcessArticle(object):
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
