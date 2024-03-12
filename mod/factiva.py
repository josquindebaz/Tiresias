""" From FACTIVA hml to Prospéro Files  TXT and CTX
Josquin Debaz
GNU General Public License
"""

import re
import os
import random

from mod.date_utils import fetch_date
from mod.file_utils import name_file, write_file, create_ctx_content

try:
    import cleaning
except ModuleNotFoundError:
    from mod.cleaning import Cleaner


def get(text, begin, end):
    """return the content between two given strings"""
    result = re.split(begin, text, 1)[1]
    result = re.split(end, result, 1)[0]
    return result


def parse(article):
    """return text and metadata"""
    result = {}
    # get title
    try:
        tag = re.search(r'<(b|span) class=["\'][a-z]{2}Headline',
                        article).group(1)
        title = get(article,
                    '<%s class=["\'][a-z]{2}Headline["\']>' % tag,
                    '</%s>' % tag)
        result['title'] = re.sub(r"^(\r\n|\n)\s*", "", title)
    except:
        result['title'] = "Title problem"
    # remove <b> and </b>
    result['title'] = re.sub(r"</?b>", "", result['title'])

    # get date and support
    divs = re.split('<div>', article)
    form1 = re.compile(r"\d{1,2}\s+[a-zéèûñíáóúüãçA-Z]*\s+\d{4}</div>")
    form2 = re.compile(r"<td>(\d{1,2}\s+[a-zéèûñíáóúüãçA-Z]*\s+\d{4})</td>")
    for div in divs:
        if form1.search(div):
            result['date'] = div[:-6]
            if re.search(r"\d{2}:\d{2}</div>", divs[divs.index(div) + 1]):
                result['time'] = u"REF_HEURE:%s" % div[:-6]
                result['media'] = divs[divs.index(div) + 2][:-6]
            else:
                result['media'] = divs[divs.index(div) + 1][:-6]
        elif form2.search(div):
            result['date'] = form2.search(div).group(1)
            result['media'] = get(article,
                                  '<b>SN</b>&nbsp;</td><td>',
                                  '</td>')
    # format date
    # result['date'] = format_date(result['date'])
    result['date'] = fetch_date(result['date'])

    # get narrator
    try:
        result['narrator'] = get(article,
                                 '<div class="author">',
                                 r'\s*</div>')
    except:
        pass

    # get text content
    result['text'] = result['title'] + "\r\n.\r\n"

    paragraphs = re.split(r'<p class="articleParagraph\s+[a-z]{2}articleParagraph"\s*>', article)

    for paragraph in paragraphs[1:]:
        paragraph = re.split("</p>", paragraph)[0]
        paragraph = re.sub(r"^(\r\n|\n)\s*", "", paragraph)
        paragraph = re.sub(r"\s*(\r\n|\n)\s*", " ", paragraph)
        paragraph = re.sub(r"</?b>", "", paragraph)  # remove <b> and </b>
        result['text'] += paragraph

    return result


class ParseHtm:
    """from htm of Factiva to Prospero"""

    def __init__(self, fname):
        self.articles = {}
        self.unknowns = []
        with open(fname, 'rb') as file:
            buf = file.read()
            buf = buf.decode('utf-8')  # byte to str
        self.content = re.split(' class="article [a-z]{2}Article">',
                                buf)[1:]
        for article in self.content:
            id_article = random.randint(0, 1000000)
            while id_article in self.articles.keys():
                id_article = random.randint(0, 1000000)
            self.articles[id_article] = parse(article)

    def get_supports(self, fname):
        """parse supports.publi and find correspondences"""
        medias = {}
        with open(fname, 'rb') as file:
            buf = file.read()
            buf = buf.decode('cp1252')  # byte to str
            lines = re.split("\r*\n", buf)
        for line in lines:
            media = re.split('; ', line)
            if media:
                medias[media[0]] = media[1:]

        for key, article in self.articles.items():
            if article['media'] in medias.keys():
                self.articles[key]['support'] = medias[article['media']][0]
                self.articles[key]['source_type'] = medias[article['media']][1]
                self.articles[key]['root'] = medias[article['media']][2]
            else:
                if article['media'] not in self.unknowns:
                    self.unknowns.append(article['media'])
                self.articles[key]['support'] = article['media']
                self.articles[key]['source_type'] = 'unknown source'
                self.articles[key]['root'] = 'FACTIVA'

    def write_prospero_files(self, save_dir=".", cleaning=False):
        """for each article, write txt and ctx in a given directory"""
        for article in self.articles.values():
            file_path = name_file(article['date'],
                                  article['root'],
                                  save_dir)

            if cleaning:
                text_cleaner = Cleaner(article['text'].encode('utf-8'))
                text = text_cleaner.content
            else:
                text = article['text']

            write_file(save_dir, file_path, ".txt", text)

            ctx = create_ctx_content(article, article['support'], article['source_type'])
            ctx = ctx.encode('latin-1', 'xmlcharrefreplace')  # to bytes
            path = os.path.join(save_dir, file_path + ".ctx")
            with open(path, 'wb') as file:
                file.write(ctx)
