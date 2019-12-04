"""Scopus to prospero
by Robin et Josquin
GPL3
04/12/2019"""

import csv
import re
import datetime
import glob

def ctx_prospero(csvfile):
    """convert ctx to prospero format files"""
    reader = csv.DictReader(csvfile, delimiter=",")
    papers = {}
    for row in reader:
        link = row['Link']
        eid = re.search(r'eid=([^\&]*)\&', link).group(1)
        papers[eid] = (row['\ufeffAuthors'], row['Title'], row['Year'],
                       row['Abstract'])

    for eid in papers:
        txt_content = papers[eid][1] + "\r\n.\r\n" + papers[eid][3]
        txt_content = txt_content.encode('latin-1', 'xmlcharrefreplace') #to bytes
        with open("%s.txt"%eid, 'wb') as txtfile:
            txtfile.write(txt_content)

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
        with open("%s.ctx"%eid, 'wb') as ctxfile:
            ctx = ctx.encode('latin-1', 'xmlcharrefreplace') #to bytes
            ctxfile.write(ctx)

if __name__ == "__main__":
    for ctx_file in glob.glob("*.csv"):
        with open(ctx_file, newline='') as csvfile:
            ctx_prospero(csvfile)
