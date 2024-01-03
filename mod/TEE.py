# -*- coding: utf-8 -*-
# Author Josquin Debaz
# GPL 3
# 28/08/2020

import urllib.request, urllib.parse
from bs4 import BeautifulSoup
import re
import datetime
import os

from cleaning import Cleaner


def formate_date(date):
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
    }

    date = date.split(' ')
    day = "%s" % ("%02d" % int(date[0]))
    return "%s/%s/%s" % (day, months[date[1]], date[2])


def formate_ctx(title, date, url):
    ctx = [
        "fileCtx0005",
        title,
        'Transitions & Energies',
        "",
        "",
        date,
        "Transitions & Energies",
        'Presse sectorielle',
        '',
        "",
        url,
        "Processed by Tiresias on %s" \
        % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "", "n", "n", ""
    ]

    return "\r\n".join(ctx)


def file_name(dest, date, prefix):
    index, base = "A", 64
    date = "".join(reversed(date.split("/")))
    name = "%s%s%s" % (prefix, date, index)
    path = os.path.join(dest, name + ".txt")
    while os.path.isfile(path):
        if ord(index[-1]) < 90:
            index = chr(ord(index[-1]) + 1)
        else:
            base += 1
            index = "A"
        if base > 64:  # if Z => 2 letters
            index = chr(base) + index
        name = "%s%s%s" % (prefix, date, index)
        path = os.path.join(dest, name + ".txt")
    return name


class ProcessArticle(object):
    def __init__(self, url):
        dest = "C:\\corpus\\EnergiCorpus\\FR\\TEE\\"
        with urllib.request.urlopen(url) as page:
            soup = BeautifulSoup(page, "lxml")
        title = soup.title.string
        author = soup.find("div", "meta-author").text
        date = soup.find("div", "meta-date").text
        title = re.sub(" - Transitions & Energies", "", title)
        print(title, author, date)
        content = title + "\r\n.\r\n\r\n"
        article = soup.find('article')
        for el in article.find_all(['h2', 'p']):
            if el.name == "h2":
                content += "\r\n\r\n" + el.text + "\r\n.\r\n"
            else:
                content += el.text

        date = formate_date(date)
        ctx = formate_ctx(title, date, url)

        ctx_cleaner = Cleaner(ctx.encode('utf-8'))
        ctx = ctx_cleaner.content.encode('latin-1', 'xmlcharrefreplace')  # to bytes

        text_cleaner = Cleaner(content.encode('utf-8'))
        text = text_cleaner.content.encode('latin-1', 'xmlcharrefreplace')  # to bytes

        filename = file_name(dest, date, "TEE")

        path = os.path.join(dest, filename + ".txt")
        with open(path, 'wb') as f:
            f.write(text)

        path = os.path.join(dest, filename + ".ctx")
        with open(path, 'wb') as f:
            f.write(ctx)


class IndexNewArticles(object):
    def __init__(self):
        self.soup = None
        to_do = "C:\\corpus\\EnergiCorpus\\FR\\TEE\\article_list.txt"
        url = "https://www.transitionsenergies.com"
        donepath = "C:\\corpus\\EnergiCorpus\\FR\\TEE\\article_retreived.txt"

        with open(donepath, 'r') as donefile:
            article_list = [line for line in re.split('\n\n', donefile.read())]
        print(len(article_list), article_list[:5])

        while url:
            print(url)

            self.get_page(url)
            list_to_do = []
            for article in self.get_articles():
                list_to_do.append(article not in article_list)
                if article not in article_list:
                    article_list.append(article)
            print(len(article_list))

            """Next page if something was new"""
            if set(list_to_do) != {False}:
                url = self.get_next()
            else:
                url = False

        with open(to_do, 'w') as list_file:
            list_file.write("\r\n".join(article_list))

    def get_page(self, url):
        with urllib.request.urlopen(url) as page:
            self.soup = BeautifulSoup(page, "lxml")

    def get_articles(self):
        articles = []
        for article in self.soup.find_all('article'):
            for link in article.find_all('a'):
                href = link['href']
                if not re.search("/category/", href) and href not in articles:
                    articles.append(href)
        return articles

    def get_next(self):
        for links in self.soup.find_all('a'):
            href = links.get('href')
            if href:
                if re.search('/page/', href):
                    return href
        return False


class IndexArticles(object):
    def __init__(self):
        self.soup = None
        dest = "C:\\corpus\\EnergiCorpus\\FR\\TEE\\article_list.txt"
        url = "https://www.transitionsenergies.com"

        article_list = []

        while url:
            print(url)
            self.get_page(url)
            for article in self.get_articles():
                if article not in article_list:
                    article_list.append(article)
            print(len(article_list))
            url = self.get_next()

        with open(dest, 'w') as list_file:
            list_file.write("\r\n".join(article_list))

    def get_page(self, url):
        with urllib.request.urlopen(url) as page:
            self.soup = BeautifulSoup(page, "lxml")

    def get_next(self):
        for links in self.soup.find_all('a'):
            href = links.get('href')
            if href:
                if re.search('/page/', href):
                    return href
        return False

    def get_articles(self):
        articles = []
        for article in self.soup.find_all('article'):
            for link in article.find_all('a'):
                href = link['href']
                if not re.search("/category/", href) and href not in articles:
                    articles.append(href)
        return articles


class RetreiveArticles(object):
    def __init__(self):
        source = "C:\\corpus\\EnergiCorpus\\FR\\TEE\\article_list.txt"
        donepath = "C:\\corpus\\EnergiCorpus\\FR\\TEE\\article_retreived.txt"
        with open(source, 'r') as sourcefile:
            to_do = [line for line in re.split('\n\n', sourcefile.read())]
            # print(to_do[:5])

        if not os.path.isfile(donepath):
            with open(donepath, 'w') as donefile:
                donefile.write("")

        with open(donepath, 'r') as donefile:
            done = [line for line in re.split('\n\n', donefile.read())]
            # print(done[:5])

        for url in to_do[0:]:
            # print(url)
            if url not in done:
                ProcessArticle(url)
                done.append(url)

                with open(donepath, 'a') as donefile:
                    donefile.write("%s\r\n" % url)


##            else:
##                print("already done")


"""
    create a list of all articles found on the website transitionsenergies.com
    store in a file  "C:\\corpus\\EnergiCorpus\\FR\\TEE\\article_list.txt"
"""
# IndexArticles()


IndexNewArticles()

"""
    Process all undone articles in the index
"""
RetreiveArticles()
