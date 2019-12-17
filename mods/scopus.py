"""Scopus to prospero
by Robin Dianoux et Josquin Debaz
GPL3
10/12/2019"""

import csv
import re
import datetime
import glob
import os

try:
    from cleaning import Cleaner
except:
    from mods.cleaning import Cleaner


def ctx_prospero(csvfile, save_dir=".",
                 cleaning=False,
                 brackets=False,
                 author_keywords=False,
                 index_keywords=False,
                 rm_copyright=False,
                 ):
    """convert ctx to prospero format files"""
    reader = csv.DictReader(csvfile, delimiter=",")
    papers = {}
    file_count = 0
    no_abstract = 0
    for row in reader:           
        link = row['Link']
        eid = re.search(r'eid=([^\&]*)\&', link).group(1)
        if row['Abstract'] == "[No abstract available]":
            no_abstract += 1
        else:
            papers[eid] = [row['Authors'],
                           row['Title'],
                           row['Year'],
                           row['Abstract'],
                           row['Author Keywords'],
                           row['Index Keywords']
                           ]

    for eid in papers:
        #remove the traductions between [] in title
        if brackets:
            papers[eid][1] = re.sub(r"\[.*\]$", "", papers[eid][1])

        #put the title at the beginning of the text
        txt_content = papers[eid][1] + "\r\n.\r\n"

        #put author keywords
        if author_keywords:
            if papers[eid][4]:
                txt_content += papers[eid][4] + "\r\n.\r\n"
                
        #put index keywords
        if index_keywords:
            if papers[eid][5]:
                txt_content += papers[eid][5] + "\r\n.\r\n"

        #remove ©
        if rm_copyright:
            papers[eid][3] = re.sub(" (©|Copyright),? \d{4},? .*$", "", papers[eid][3])                
                
        #put text content
        txt_content += papers[eid][3]

        if cleaning:
            text_cleaner = Cleaner(txt_content.encode('utf-8'))
            txt_content = text_cleaner.content
        txt_content = txt_content.encode('latin-1',
                                         'xmlcharrefreplace') #to bytes
        filename = os.path.join(save_dir, eid)
        with open("%s.txt"%filename, 'wb') as txtfile:
            txtfile.write(txt_content)
            file_count += 1

        ctx = [
            "fileCtx0005",
            papers[eid][1],
            papers[eid][0],
            "", "",
            "01/01/%s"%papers[eid][2],
            "",
            "",
            "", "", "",
            "From Scopus by Tiresias on %s"\
                % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "", "n", "n", ""
            ]
        ctx = "\r\n".join(ctx)
        with open("%s.ctx"%filename, 'wb') as ctxfile:
            ctx = ctx.encode('latin-1', 'xmlcharrefreplace') #to bytes
            ctxfile.write(ctx)
            file_count += 1

    return file_count, no_abstract

if __name__ == "__main__":
    for ctx_file in glob.glob("*.csv"):
        with open(ctx_file, newline='', encoding='utf-8-sig') as csvfile:
            #encoding='utf-8-sig' against BOM saved file that generate a "ï»¿"
            file_count, no_abstract = ctx_prospero(csvfile,
                                                   cleaning=True,
                                                   brackets=True,
                                                   author_keywords=True,
                                                   index_keywords=True,
                                                   rm_copyright=True)
            print("Created %d file(s), skipped %d articles with no abstract"\
                  %(file_count, no_abstract))
