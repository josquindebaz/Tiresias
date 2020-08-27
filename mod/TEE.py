# -*- coding: utf-8 -*-
# Author Josquin Debaz
# GPL 3
#27/08/2020

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
    day = "%s"%("%02d" % int(date[0]))
    return "%s/%s/%s"%(day, months[date[1]], date[2])

def formate_ctx(title, date):
    ctx = [
        "fileCtx0005",
        title,
        'Transitions & Energies',
        "", "",
        date,
        "Transitions & Energies",
        'Presse sectorielle',
        '',
        "", "",
        "Processed by Tiresias on %s"\
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
        if (ord(index[-1]) < 90):
            index = chr(ord(index[-1]) + 1)
        else:
            base += 1   
            index = "A"    
        if base > 64 : #if Z => 2 letters
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
        content = title +  "\r\n.\r\n\r\n"
        article = soup.find('article')
        for el in article.find_all(['h2', 'p']):
            if el.name == "h2":
                content += "\r\n\r\n" + el.text  + "\r\n.\r\n"
            else:
                content += el.text

        date = formate_date(date)
        ctx = formate_ctx(title, date)

        ctx_cleaner =  Cleaner(ctx.encode('utf-8'))
        ctx = ctx_cleaner.content.encode('latin-1', 'xmlcharrefreplace') #to bytes

        text_cleaner =  Cleaner(content.encode('utf-8'))
        text = text_cleaner.content.encode('latin-1', 'xmlcharrefreplace') #to bytes


        filename = file_name(dest, date, "TEE")
        
        path = os.path.join(dest, filename + ".txt")
        with open(path, 'wb') as f:
            f.write(text)
            
        path = os.path.join(dest, filename + ".ctx")        
        with open(path, 'wb') as f:
            f.write(ctx)




        


    

url = "https://www.transitionsenergies.com/renouvelables-trop-ou-trop-peu-electricite/"
ProcessArticle(url)

