"""Scopus to prospero
by Robin Dianoux et Josquin Debaz
GPL3
04/12/2019"""

import csv
import re
import datetime
import glob
import os


def ctx_prospero(csvfile, save_dir="."):
    """convert ctx to prospero format files"""
    reader = csv.DictReader(csvfile, delimiter=",")
    papers = {}
    file_count = 0
    for row in reader:           
        link = row['Link']
        eid = re.search(r'eid=([^\&]*)\&', link).group(1)
        papers[eid] = (row['Authors'], row['Title'], row['Year'],
                       row['Abstract'])

    for eid in papers:
        txt_content = papers[eid][1] + "\r\n.\r\n" + papers[eid][3]
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

    return file_count

if __name__ == "__main__":
    for ctx_file in glob.glob("*.csv"):
        with open(ctx_file, newline='', encoding='utf-8-sig') as csvfile:
            #encoding='utf-8-sig' against BOM saved file that generate a "ï»¿"
            ctx_prospero(csvfile)
