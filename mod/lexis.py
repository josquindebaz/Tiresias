"""From Lexis txt to Prospéro Files  TXT and CTX
by Josquin Debaz
GPL3
09/12/2019"""

import glob
import random
import re
import os
import datetime

try:
    from cleaning import Cleaner
except:
    from mod.cleaning import Cleaner


def format_date(date):
    """return the number of a french or English or German month"""
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
        "December": "12",
        "Januar": "01",
        'Februar': "02",
        "März": "03",
        "Mai": "05",
        "Juni": "06",
        "Juli": "07",
        # "August": "08", # duplicated
        "Oktober": "10",
        "Dezember": "12"
    }
    try:
        date = re.split(" ", date)
        day = "%02d" % int(date[0][:-1])  # day with 2 digits
        return "%s/%s/%s" % (day, months[date[1]], date[2][:4])
    except:
        return "00/00/0000"


def file_name(date, prefix, save_dir):
    """return a name in Prospero style"""
    index, base = "A", 64
    date = "".join(reversed(date.split("/")))
    name = "%s%s%s" % (prefix, date, index)
    path = os.path.join(save_dir, name + ".txt")
    while os.path.isfile(path):
        if ord(index[-1]) < 90:
            index = chr(ord(index[-1]) + 1)
        else:
            base += 1
            index = "A"
        if base > 64:  # if Z => 2 letters
            index = chr(base) + index
        name = "%s%s%s" % (prefix, date, index)
        path = os.path.join(save_dir, name + ".txt")
    return name


class ParseTxt(object):
    """from txt of Lexis to Prospero"""

    def __init__(self, filename):
        self.articles = {}
        self.unknowns = []
        self.count = 0
        with open(filename, 'rb') as file:
            buf = file.read()
            buf = buf.decode('utf-8')  # byte to str
        cut_articles = re.split(r"(.*Do[kc]ument \d+ (von|de|of) \d+.*)", buf)[1:]
        while cut_articles:
            self.count += 1
            cut_articles.pop(0)  # number
            cut_articles.pop(0)  # language mark
            id_article = random.randint(0, 1000000)
            while id_article in self.articles.keys():
                id_article = random.randint(0, 1000000)
            self.articles[id_article] = \
                self.process(cut_articles.pop(0))  # content

    def get_supports(self, supports_path):
        """parse supports.publi and find correspondences"""
        medias = {}
        with open(supports_path, 'rb') as file:
            buf = file.read()
            buf = buf.decode('cp1252')  # byte to str
            lines = re.split("\r*\n", buf)
        for line in lines:
            media = re.split('; ', line[:-1])
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
                self.articles[key]['root'] = 'LEXIS'

    def process(self, content):
        head, waste, article = "", "", ""

        if re.search(r"\r\n(LÄNGE|LENGTH|LONGUEUR): \d* \S*\r\n", content):
            head, waste, article = re.split(r'\r\n(LÄNGE|LENGTH|LONGUEUR): \d* \S*\r\n',
                                            content, 1)

        if re.search("\r\nUPDATE:.*\r\n", article):
            article, foot = re.split("UPDATE:", article)
        elif re.search("\r\nLOAD-DATE:.*\r\n", article):
            article, foot = re.split("LOAD-DATE:", article)

        # Internationaliser ?
        # def traite_article(self,article):
        #     article = re.split('\r\nDATE-CHARGEMENT:',article)[0]
        #     if re.search("ORIGINE-DEPECHE:",article):
        #             en_tete,article = re.split('\r\nORIGINE-DEPECHE: .*\r\n',article,1)
        #     elif re.search("\r\nLONGUEUR: \d* \S*\r\n",article):
        #             en_tete,article = re.split('\r\n: \d* \S*\r\n',article,1)
        #     elif re.search('\r\nRUBRIQUE: .*\r\n',article):
        #             en_tete,article = re.split('\r\nRUBRIQUE: .*\r\n',article,1)

        # sous-titre ?

        article_data = {'text': re.sub(r"HIGHLIGHT:\s*", "", article)}

        metas = re.split(r"\r?\n\r\n\s*", head)
        article_data["media"] = metas[1]
        article_data["date"] = format_date(metas[2])
        article_data["title"] = metas[3]

        if len(metas) > 4:
            for item in metas[4:]:
                if re.match("(AUTOR|AUTEUR): ", item):
                    article_data["narrator"] = item
                    article_data["narrator"] = re.sub("(AUTOR|AUTEUR): ", "",
                                                      article_data["narrator"])

        return article_data

    def write_prospero_files(self, save_dir=".", cleaning=False):
        """for each article, write txt and ctx in a given directory"""
        for article in self.articles.values():
            filepath = file_name(article['date'],
                                 article['root'],
                                 save_dir)
            path = os.path.join(save_dir, filepath + ".txt")

            article['text'] = article['title'] + "\r\n.\r\n" + article['text']
            if cleaning:
                text_cleaner = Cleaner(article['text'].encode('utf-8'))
                text = text_cleaner.content
            else:
                text = article['text']
            with open(path, 'wb') as file:
                # to bytes
                file.write(text.encode('latin-1', 'xmlcharrefreplace'))
            ctx = [
                "fileCtx0005",
                article['title'],
                article['support'],
                "", "",
                article['date'],
                "",
                article['source_type'],
                "", "", "",
                f"Processed by Tiresias on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "", "n", "n", ""
            ]
            ctx = "\r\n".join(ctx)
            ctx = ctx.encode('latin-1', 'xmlcharrefreplace')  # to bytes
            path = os.path.join(save_dir, filepath + ".ctx")
            with open(path, 'wb') as file:
                file.write(ctx)


if __name__ == '__main__':
    SUPPORTS_FILE = "../data/support.publi"
    for filename in glob.glob("*.txt"):
        print("Processing " + filename)
        parse = ParseTxt(filename)
        parse.get_supports(SUPPORTS_FILE)
        print("%d unknown(s) source(s)" % len(parse.unknowns))
        for unknown in parse.unknowns:
            print("unknown: %s" % unknown)
        parse.write_prospero_files("C:\\Users\\gspr\\Desktop\\traitement")
