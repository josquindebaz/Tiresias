# -*- coding: utf-8 -*-
# Author Josquin Debaz
# GPL 3

import urllib.request, urllib.parse
from bs4 import BeautifulSoup
import re
import datetime
import os


        
def file_name(date, prefix):
    index, base = "A", 64
    date = "".join(reversed(date.split("/")))
    name = "%s%s%s" % (prefix, date, index)
    path = name + ".txt"
    while os.path.isfile(path):
        if (ord(index[-1]) < 90):
            index = chr(ord(index[-1]) + 1)
        else:
            base += 1   
            index = "A"    
        if base > 64 : #if Z => 2 letters
            index = chr(base) + index
        name = "%s%s%s" % (prefix, date, index)
        path = name + ".txt"
    return name

#url = "https://www.transitionsenergies.com/renouvelables-trop-ou-trop-peu-electricite/"
#url = "https://www.transitionsenergies.com/long-terme-geothermie-gagne/"
#print(urllib.request.urlretrieve(url, "TE2.html"))


with open("TE2.html", 'r') as page:
    soup = BeautifulSoup(page, "lxml")
    title = soup.title.string
    author = soup.find("div", "meta-author").text
    date = soup.find("div", "meta-date").text
    title = re.sub(" - Transitions & Energies", "", title)
    print(title, author, date)
    content = title +  "\n.\n\n"
    article = soup.find('article')
    for el in article.find_all(['h2', 'p']):
        if el.name == "h2":
            content += "\n\n" + el.text  + "\n.\n"
        else:
            content += el.text
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
date = "%s/%s/%s"%(day, months[date[1]], date[2])


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

ctx = "\r\n".join(ctx)

ctx = ctx.encode('latin-1', 'xmlcharrefreplace') #to bytes
text = content.encode('latin-1', 'xmlcharrefreplace') #to bytes


path = file_name(date, "TEE")

with open(path + '.txt', 'wb') as f:
    f.write(text)
            
with open(path + '.ctx', 'wb') as f:
    f.write(ctx)


