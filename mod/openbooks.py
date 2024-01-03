# -*- coding: utf-8 -*-
"""
From Open edition books to Prospéro Files  TXT and CTX
Author Josquin Debaz
GNU General Public License
Version 3, 29 June 2007
08/12/2020
"""

import datetime
import os
import re
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

try:
    from cleaning import Cleaner
except:
    from mod.cleaning import Cleaner


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


def extract_chapter(soup):
    titre = soup.find("h1", "title").text
    text = titre + "\r\n.\r\n\r\n"
    notes = {}
    notesoup = soup.find("div", {"id": "notes"})
    if notesoup:
        for note in notesoup.find_all("p"):
            notes[note.a.text] = " ".join([str(el.string).strip()
                                           for el in note.contents[1:]])

    for paragraph in soup.find_all("p", {"class": "texte"}):
        if not paragraph.find("a", {"class": "FootnoteSymbol"}):
            for node in paragraph.children:
                if node.name != 'span':
                    if node.name == "a":
                        if "class" in node.attrs:
                            if node["class"] == ['footnotecall']:
                                text += " [%s] " % re.sub(".$", "",
                                                          notes[node.string])
                        else:
                            # print(node.attrs)
                            pass
                    else:
                        try:
                            text += node.string
                        except:
                            text += str(node.string)
        text += "\r\n\r\n"
    return text


def get_soup(url):
    with urllib.request.urlopen(url) as page:
        return BeautifulSoup(page, "lxml")


def create_ctx(path, metadata):
    ctx = [
        "fileCtx0005",
        metadata['title'],
        metadata['authors'],
        "",
        "",
        "01/01/" + metadata['date'],
        "",
        "chapitre",
        metadata['ref'],
        "",
        "",
        f"Processed by Tiresias on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "", "n", "n", ""
    ]
    ctx = "\r\n".join(ctx)
    ctx_cleaner = Cleaner(ctx.encode('utf-8'))
    ctx = ctx_cleaner.content.encode('latin-1', 'xmlcharrefreplace')  # to bytes
    with open(path, 'wb') as file:
        file.write(ctx)


def write_txt(path, text):
    text_cleaner = Cleaner(text.encode('utf-8'))
    text = text_cleaner.content.encode('latin-1', 'xmlcharrefreplace')  # to bytes
    # text = text.encode('latin1', errors='xmlcharrefreplace')
    with open(path, 'wb') as f:
        f.write(text)


def teste_sommaire(soup):
    if soup.find("li", {"id": "link-more-content-sommaire"}):
        return True
    return False


def get_chapters(soup):
    sommaire = soup.find("div", {"id": "book-more-content-sommaire"})
    return [item.a["href"] for item
            in sommaire.find_all("div", "chapter")]


def create_chapter_urls(url, chapters):
    root = re.sub(r"\d*$", "", url)
    return [root + chapter for chapter in chapters]


def get_authors(soup):
    authors = soup.find_all("div", "name")
    if not authors:
        authors = soup.find_all("meta", {"name": "author"})
        authors = [" ".join(reversed(author["content"].split(', ')))
                   for author in authors]
    else:
        authors = [author.text.strip() for author in authors]
    return ", ".join(authors)


def get_citing(soup):
    mla = soup.find("div", {"id": "citation-chapter-mla"})
    mla = mla.text.strip()
    return mla


def get_metadata(soup):
    return {"authors": get_authors(soup), "title": soup.find("meta", {"name": "DC.title"})["content"].strip(),
            "date": soup.find("meta", {"name": "DC.date"})["content"], "ref": get_citing(soup)}


def traite_url(url, save_dir="."):
    soup = get_soup(url)
    if not teste_sommaire(soup):
        # print("\tis a chapter")
        metadata = get_metadata(soup)
        chapter = extract_chapter(get_soup(url))
        chapter_number = re.search(r"\d*$", url).group(0)
        chap_name = chapter_number + metadata["authors"].split()[1]
        filename = file_name(save_dir, "01/01/" + metadata["date"], chap_name)
        path = os.path.join(save_dir, filename + ".txt")
        write_txt(path, chapter)
        path = os.path.join(save_dir, filename + ".ctx")
        create_ctx(path, metadata)
    else:
        # print("\tis a frontpage")
        chapters = get_chapters(soup)
        chapter_urls = create_chapter_urls(url, chapters)
        for chapter_url in chapter_urls:
            traite_url(chapter_url, save_dir)


if __name__ == "__main__":
    # url = "https://books.openedition.org/igpde/6841"
    #    url = "https://books.openedition.org/igpde/6486"
    #    url = "http://books.openedition.org/igpde/6591"
    url = "https://books.openedition.org/editionsmsh/12006"
    # url = "https://books.openedition.org/editionsmsh/12030"
    # url = "https://books.openedition.org/enseditions/12892"
    traite_url(url, "C:\\Users\\gspr\\Desktop\\traitement")
