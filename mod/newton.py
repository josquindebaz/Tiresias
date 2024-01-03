"""
Script for html from Newton for Prospero
Create TXT and CTX from html in the directory
previous version for Python2 16 april 2018 
by Josquin Debaz
GPL3
13/12/2019
modified 12/05/2021
"""

import glob
import random
import re
import os
import datetime
from bs4 import BeautifulSoup

try:
    from cleaning import Cleaner
except:
    from mod.cleaning import Cleaner


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


class parseNewton(object):
    def __init__(self, filename):
        self.articles = {}
        self.unknowns = []
        self.count = 0
        with open(filename, 'rb') as file:
            buf = file.read()
            buf = buf.decode('utf-8')  # byte to str
        articles = self.get_articles(buf)
        for article in articles:
            self.count += 1

            id_article = random.randint(0, 1000000)
            while id_article in self.articles.keys():
                id_article = random.randint(0, 1000000)
            self.articles[id_article] = self.process(article)  # content

    def get_articles(self, text):
        soup = BeautifulSoup(text, 'lxml')
        tables = soup.find_all("table",
                               attrs={"style": "margin-top: 15px"})
        articles = [table for table in tables
                    if len(table.find_all('tr')) == 3]

        print("found %s articles" % len(articles))
        for article in articles:
            yield article

    def replace_cz(self, text):
        ##        latin1 = text.encode('ISO-8859-1', 'xmlcharrefreplace')
        ##        text = latin1.decode('ISO-8859-1')

        latin2 = text.encode('iso-8859-2', 'xmlcharrefreplace')
        text = latin2.decode('iso-8859-2')

        table = {
            ##            '&#268;': 'Č',
            ##            '&#269;': 'č',
            ##            '&#271;': "d'",
            ##            "&#282;": 'Ě',
            ##            "&#283;": 'ě',
            ##            '&#328;': 'ň',
            ##            '&#344;': 'Ř',
            ##            "&#345;": 'ř',
            ##            '&#352;': 'Š',
            ##            '&#353;': 'š',
            ##            '&#357;': "ť",
            ##            '&#366;': 'Ů',
            ##            '&#367;': 'ů',
            ##            '&#381;': 'Ž',
            ##            '&#382;': 'ž',
            '&#8211;': '-',
            '&#8216;': "'",
            '&#8218;': "'",
            '&#8220;': '"',
            '&#8222;': '"',
            '&#8230;': '...',
            '&amp;': '&',
        }
        for xml, replace in table.items():
            text = re.sub(xml, replace, text)
        if re.search(r"&#\d*;", text):
            print("Don't know how to replace :",
                  ", ".join(re.findall(r"&#\d*;", text)))
        return text

    def process(self, content):
        article_data = {"title": content.find('a').text.strip()}

        for meta_data in content.find_all(class_="metadata-item"):
            if re.search(r', Datum:\s\d', meta_data.text):
                article_data["date"] = re.sub(r'\.', r'/',
                                              meta_data.find('span').text)
            elif re.search(r', Zdroj:', meta_data.text):
                article_data["media"] = re.sub(r'\.', r'/',
                                               meta_data.find('span').text)
            elif re.search(r', Autor:', meta_data.text):
                article_data["narrator"] = re.sub(r'\.', r'/',
                                                  meta_data.find('span').text)
        ##            else:
        ##                print(meta_data)
        article_data["observations"] = ""
        article_data['text'] = content.find(class_="article-content").text.strip()
        return {element: self.replace_cz(value)
                for element, value in article_data.items()}

    ##    def get_articles_old(self, text):
    ##        articles = re.split('<hr size="1"', text)[2:-1]
    ##        for article in articles:
    ##            yield article

    ##    def process_old(self, content):
    ##        article_data = {}
    ##        content = self.replace_cz(content)
    ##
    ##        metadata, text = re.split("<em>zpet</em>", content)
    ##        article_data["title"] =\
    ##            re.findall('<a name="\d*">.*>(.*)</a>.*size="2">', metadata)[0]
    ##        date = re.split("\.",
    ##                        re.findall('>([\d\.]*)&nbsp;&nbsp;', metadata)[0])
    ##        article_data["date"] =  "%02d/%02d/%s"%(int(date[0]),
    ##                                                int(date[1]),
    ##                                                date[2])
    ##        splitted = re.split('&nbsp;&nbsp;(.*)</font>', metadata)[1]
    ##        article_data["media"] = re.findall('(.*)\&nbsp;&nbsp;str', splitted)[0]
    ##        article_data["observations"] = re.findall('\d&nbsp;&nbsp;(.*)</font>',
    ##                                                  splitted)[0]
    ##        article_data["narrator"] = re.findall('<em>(.*)</em>', splitted)[0]
    ##
    ##        text = re.split('<font face="Arial" size="2">', text)[1]
    ##        text = re.split('</td>', text)[0]
    ##        text = re.sub('<br />', '', text)
    ##        text = re.sub('<strong><span style="background-color: #fac900; color: #000000;">', '', text)
    ##        text = re.sub('</span></strong>', '', text)
    ##        article_data['text'] = text
    ##
    ##        return article_data

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
                self.articles[key]['root'] = 'NEWTON'

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

            # to bytes
            text = text.encode('iso-8859-2', 'xmlcharrefreplace')
            with open(path, 'wb') as file:
                file.write(text)
            ctx = [
                "fileCtx0005",
                article['title'],
                article['support'],
                "", "",
                article['date'],
                "",
                article['source_type'],
                article["observations"],
                "", "",
                "Processed by Tiresias on %s" \
                % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "", "n", "n", ""
            ]
            ctx = "\r\n".join(ctx)
            ctx = ctx.encode('iso-8859-2', 'xmlcharrefreplace')  # to bytes
            path = os.path.join(save_dir, filepath + ".ctx")
            with open(path, 'wb') as file:
                file.write(ctx)


if __name__ == '__main__':
    SUPPORTS_FILE = "../data/support.publi"
    for filename in glob.glob("*.html"):
        print("Processing " + filename)
        parse = parseNewton(filename)
        parse.get_supports(SUPPORTS_FILE)
        print("%d unknown(s) source(s)" % len(parse.unknowns))
        for unknown in parse.unknowns:
            print("unknown: %s" % unknown)
        parse.write_prospero_files(".")
