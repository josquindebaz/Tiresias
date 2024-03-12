import html
import re

from mod.date_utils import fetch_date
from utils.supportpublimanager import SupportPubliManager
from mod.file_utils import name_file, write_file, create_ctx_content, clean_content


def format_support_name(support):
    motif = re.compile(r"\s*([<(,]).*$")
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


def get_header_infos(header):
    infos = {}

    publication_name = in_tag(header, "DocPublicationName")
    infos["source"] = format_support_name(publication_name)

    infos["date"] = fetch_date(in_tag(header, "DocHeader"))

    title = in_tag(header, "titreArticle")
    title = strip_tags_with_class(title)
    title = re.sub(r"\s+", " ", title)
    title = title.strip()
    infos["title"] = strip_tags_with_class(title)

    infos["narrator"] = in_tag(header, "docAuthors")

    infos["subtitle"] = False
    m_subtitle = re.compile("<b><p>(.*)</p></b>")
    if m_subtitle.search(header):
        infos["subtitle"] = m_subtitle.search(header).group(1)

    return infos


def is_plain_article(raw_article):
    if re.search('<p class="link-not-hosted">', raw_article):
        # print("only a link")
        return False
    elif re.search('class="DocPublicationName">(Rapports|Reports) -', raw_article):
        # print("only a report extract")
        return False
    elif re.search('<div class="twitter">', raw_article):
        # print("only a tweet")
        return False

    return True


class EuropresseArticleParser:
    def __init__(self, article):
        self.header = ""
        self.result = False

        if is_plain_article(article):
            self.parse_article(article)

    def parse_article(self, raw_article):
        article_content = html.unescape(raw_article)
        header, body = re.split('</header>', article_content)

        self.result = get_header_infos(header)

        text = in_tag(body, "docOcurrContainer")
        self.result["text"] = strip_tags_with_class(text)

    @property
    def get_result(self):
        return self.result


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
            article_parser = EuropresseArticleParser(article)
            parsed = article_parser.get_result
            if parsed:
                self.parsed_articles.append(parsed)


def fetch_publication_infos(publication):
    publication_index = SupportPubliManager()

    if publication not in publication_index.codex.keys():
        return "EUROPRESSE", publication, "unknown source"

    prefix = publication_index.codex[publication]['abr']
    source = publication_index.codex[publication]['source']
    source_type = publication_index.codex[publication]['type']

    return prefix, source, source_type


def create_txt_content(article):
    result = article['title'] + "\r\n.\r\n"
    result += article['subtitle'] + "\r\n.\r\n" if article['subtitle'] else ""
    result += article['text']

    return result




class EuropresseProsperoFileWriter(object):
    def __init__(self, article, destination, cleaning_required=True):

        prefix, source, source_type = fetch_publication_infos(article['source'])
        self.filename = name_file(article['date'], prefix, destination)

        txt_content = create_txt_content(article)
        ctx_content = create_ctx_content(article, source, source_type)

        cleaned_ctx_content, cleaned_txt_content = clean_content(cleaning_required,
                                                                 ctx_content,
                                                                 txt_content)

        write_file(destination, self.filename, ".txt", cleaned_txt_content)
        write_file(destination, self.filename, ".ctx", cleaned_ctx_content)

    @property
    def get_filename(self):
        return self.filename
