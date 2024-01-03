""" From FACTIVA hml to Prospéro Files  TXT and CTX
Josquin Debaz
GNU General Public License
Version 3, 29 June 2007
"""

import re
import os
import glob
import random
import datetime
import csv
import pandas as pd

try:
    import cleaning
except:
    from mod.cleaning import Cleaner


def get(text, begin, end):
    """return the content between two given strings"""
    result = re.split(begin, text, 1)[1]
    result = re.split(end, result, 1)[0]
    return result


def format_date(date):
    """return the number of a French or English mouth"""
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
    try:
        date = re.split(" ", date)
        day = "%02d" % int(date[0])  # day with 2 digits
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
        result['title'] = re.sub(r"\s*(\r\n|\n)\s*$", "", result['title'])
        result['title'] = re.sub(r"\s+", " ", result['title'])
        result["title"] = str(result["title"]).strip()
    except:
        result['title'] = "Title problem"
    # remove <b> and </b>
    result['title'] = re.sub(r"</?b>", "", result['title'])
    # get date and support
    divs = re.split('<div>', article)
    form1 = re.compile(r"\d{1,2}\s+[a-zéèûñíáóúüãçA-Z]*\s+\d{4}</div>")
    form2 = re.compile(r"<td>(\d{1,2}\s+[a-zéèûñíáóúüãçA-Z]*\s+\d{4})</td>")
    c = 0
    for div in divs:

        chaves = ["CLM", "SE", "HD", "BY", "CR", "WC", "PD", "SN", "SC", "ED", "PG", "LA", "CY", "LP", "TD", "ART",
                  "CO", "IN", "NS", "RE", "IPC", "IPD", "PUB", "AN"]
        for chave in chaves:
            div_name = f"<b>{chave}</b>&nbsp;</td><td>"
            if div_name in div:
                v = get(div, div_name, "</td></tr>")
                v = str(v).strip()
                v = v.replace("<br/>", "").replace("</span>", "")
                v = re.sub(r"</?b>", "", v)
                v = re.sub(r"</?span[^>]*>", "", v)
                v = re.sub(r"</?font[^>]*>", "", v)
                v = re.sub(r"<br[^>]*>", "", v)
                result[chave] = v
            else:
                result[chave] = ""

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
        else:
            result['date'] = result["PD"]
            result['media'] = result["SN"]
    # format date

    result['date'] = format_date(result['date'])
    # get narrator
    try:
        result['narrator'] = get(article,
                                 '<div class="author">',
                                 r'\s*</div>')
    except:
        pass

    paragraphs = re.split('<p class="articleParagraph [a-z]{2}\
articleParagraph" >', article)[1:]
    if not paragraphs:
        paragraphs = re.split('<p class="articleParagraph [a-z]{2}\
articleParagraph">', article)[1:]
    # get text content
    result['text'] = result['title'] + "\r\n.\r\n" + "LP: "

    for idx, paragraph in enumerate(paragraphs):
        p = paragraph
        paragraph = re.split("</p>", paragraph)[0]
        paragraph = re.sub(r"^(\r\n|\n)\s*", "", paragraph)
        paragraph = re.sub(r"\s*(\r\n|\n)\s*", " ", paragraph)
        paragraph = re.sub(r"</?b>", "", paragraph)  # remove <b> and </b>
        # removendo span
        paragraph = re.sub(r"</?span[^>]*>", "", paragraph)
        lp = p if "</td><td>" in p else ""
        if lp:
            if idx < len(paragraphs) - 1:
                result["LP"] = paragraph
                paragraph = paragraph + "\r\n" + "TD: "
        result['text'] += paragraph
    texto = str(str(result['text']).split('LP:')[1]).split('TD:')
    result["LP"] = texto[0]
    result["TD"] = texto[1]
    result["text"] = result["text"].replace("LP: ", "").replace("TD: ", "")
    return result


class ParseCsv:
    """from htm of csv to Prospero"""

    def __init__(self, fname):
        self.content = pd.read_csv(fname, sep=";", encoding="utf-8")

    # def get_supports(self, fname):
    #     """parse supports.publi and find correspondences"""
    #     medias = {}
    #     with open(fname, 'rb') as file:
    #         buf = file.read()
    #         try:
    #             buf = buf.decode('utf8') #byte to str
    #         except:
    #             buf = buf.decode('latin-1')
    #         lines = re.split("\r*\n", buf)
    #     for line in lines:
    #         media = re.split('; ', line)
    #         if media:
    #             medias[media[0]] = media[1:]

    #     for key, article in self.articles.items():
    #         if article['media'] in medias.keys():
    #             self.articles[key]['support'] = medias[article['media']][0]
    #             self.articles[key]['source_type'] = medias[article['media']][1]
    #             self.articles[key]['root'] = medias[article['media']][2]
    #         else:
    #             if article['media'] not in self.unknowns:
    #                 self.unknowns.append(article['media'])
    #             self.articles[key]['support'] = article['media']
    #             self.articles[key]['source_type'] = 'unknown source'
    #             self.articles[key]['root'] = 'FACTIVA'

    def write_prospero_files(self, save_dir=".", cleaning=False):
        """for each article, write txt, csv and ctx in a given directory"""

        for _, row in self.content.iterrows():
            filepath = file_name(str(row['PD']).replace('/', ''),
                                 "FACTIVA",
                                 save_dir)
            path = os.path.join(save_dir, filepath + ".txt")

            with open(path, 'wb') as file:
                titulo = str(row['HD']) + "\r\n"
                ponto = ".\r\n"
                subtitulo = str(row["LP"]) + "\r\n"
                texto = str(row["TD"])
                file.write(titulo.encode('utf8'))
                file.write(ponto.encode('utf8'))
                file.write(subtitulo.encode('utf8'))
                file.write(texto.encode('utf8'))

            ed = f'\ ED: {row["ED"]}'
            pg_se = f'PG: {row["PG"]} / SE: {row["SE"]} '.replace("\\", " ")
            ctx = [
                "fileCtx0005",  # 1
                str(row['HD']).strip(),  # 2
                f"{row['SN']}",  # 3
                f"{row['BY']}",  # 4
                "",  # 5
                f"{row['PD']}",  # 6
                f"{row['SN']}",  # 7
                "", "",  # 8, #9
                pg_se,  # 10
                "",  # 11,
                # article['source_type'],
                # "", "", "",
                "Processed by Tiresias on %s" \
                % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 12
                "", "n", "n",  # 13, #14, #15
            ]
            ctx = "\r\n".join(ctx)
            ctx = ctx.encode('utf8', 'xmlcharrefreplace')  # to bytes
            path = os.path.join(save_dir, filepath + ".ctx")
            with open(path, 'wb') as file:
                file.write(ctx)


if __name__ == "__main__":
    SUPPORTS_FILE = "support.publi"
    for filename in glob.glob("*.csv"):
        print(filename)
        run = ParseCsv(filename)
        # print("%s: found %d article(s)"%(filename, len(run.content)))
        # run.get_supports(SUPPORTS_FILE)
        # print("%d unknown(s) source(s)" %len(run.unknowns))
        # for unknown in run.unknowns:
        #     print("unknown: %s" % unknown)
        # run.write_prospero_files(".")
