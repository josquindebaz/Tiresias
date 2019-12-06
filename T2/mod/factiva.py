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


class parse_htm(object):
    "from htm of factiva to Prospero"
    def __init__(self, filename):
        self.articles = {}
        with open(filename, 'rb') as file:
            buf = file.read()
            buf = buf.decode('utf-8') #byte to str
        self.content = re.split(' class="article [a-z]{2}Article">',
                            buf)[1:]
        for article in self.content:
            self.articles[random.randint(0, 1000000)] = self.parse(article)       

    def get(self, text, begin, end):
        result = re.split(begin, text, 1)[1]
        result = re.split(end, result, 1)[0]
        return result

    def format_date(self, date):
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
            day = "%02d"%int(date[0]) #day with 2 digits
            return "%s/%s/%s" % (day, months[date[1]], date[2][:4])
        except:
            return "00/00/0000"
            

    def parse(self, article):
        result = {}
        #get title
        try:
            tag = re.search(r'<(b|span) class=["\'][a-z]{2}Headline',
                                article).group(1)
            title = self.get(article,
                             '<%s class=["\'][a-z]{2}Headline["\']>'%tag,
                             '</%s>'%tag)
            result['title'] = re.sub("^(\r\n|\n)\s*", "", title)
        except:
            result['title'] = "Title problem"
        #remove <b> and </b>
        result['title'] = re.sub(r"</?b>", "", result['title'])
        
        #get date and support
        divs = re.split('<div>', article)
        for div in divs:
            if re.search("\d{1,2}\s{1,}[a-zéèûñíáóúüãçA-Z]*\s{1,}\d{4}</div>",
                         div):
                result['date'] = div[:-6]
                if re.search("\d{2}:\d{2}</div>", divs[divs.index(div)+1]):
                    result['time'] = u"REF_HEURE:%s" % div[:-6]
                    result['media'] = divs[divs.index(div)+2][:-6]
                else :
                    result['media'] = divs[divs.index(div)+1][:-6]
            elif re.search("<td>\d{1,2}\s{1,}\
[a-zéèûñíáóúüãçA-Z]*\s{1,}\d{4}</td>",
                           div):
                    result['date'] = re.search("<td>(\d{1,2}\s{1,}\
[a-zéèûñíáóúüãçA-Z]*\s{1,}\d{4})</td>",
                                     div).group(1)
                    result['media'] = self.get(article,
                                         '<b>SN</b>&nbsp;</td><td>',
                                         '</td>')
        #format date
        result['date'] = self.format_date(result['date'])

        #get narrator
        try:
            result['narrator'] = self.get(article,
                                          '<div class="author">',
                                          '\s*</div>')
        except:
            pass
        
        #get text content
        result['text'] = result['title'] + "\r\n.\r\n"
        for paragraph in re.split('<p class="articleParagraph [a-z]{2}\
articleParagraph">', article)[1:]:
            paragraph = re.split("</p>", paragraph)[0]
            paragraph = re.sub(r"^(\r\n|\n)\s*", "", paragraph)
            paragraph = re.sub(r"\s*(\r\n|\n)\s*", " ", paragraph)
            paragraph = re.sub(r"</?b>", "", paragraph)#remove <b> and </b>
            result['text'] += paragraph

        return result               

    def get_supports(self, filename):
        medias = {}
        self.unknowns = []
        with open(filename, 'rb') as file:
            buf = file.read()
            buf = buf.decode('cp1252') #byte to str
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
                self.articles[key]['root'] = 'FACTIVA'

    def file_name(self, date, prefix):
        index, base = "A", 64
        date = "".join(reversed(date.split("/")))
        name = "%s%s%s" % (prefix, date, index)
        path = os.path.join(self.dest, name + ".txt")
        while os.path.isfile(path):
            if (ord(index[-1]) < 90):
                index = chr(ord(index[-1]) + 1)
            else:
                base += 1   
                index = "A"    
            if base > 64 : #if Z => 2 letters
                index = chr(base) + index
            name = "%s%s%s" % (prefix, date, index)
            path = os.path.join(self.dest, name + ".txt")
        return name

    def write_prospero_files(self, save_dir="."):
        self.dest = save_dir
        for key, article in self.articles.items():
            filename = self.file_name(article['date'], article['root'])
            path = os.path.join(self.dest, filename + ".txt")
            text = article['text'].encode('latin-1', 'xmlcharrefreplace') #to bytes
            with open(path, 'wb') as file:
                file.write(text)
            ctx = [
                "fileCtx0005",
                article['title'],
                article['support'],
                "","",
                article['date'],
                "",
                article['source_type'],
                "", "", "",
                "Processed by Tiresias on %s"\
                    % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "", "n","n", ""
                ]
            ctx = "\r\n".join(ctx)
            ctx = ctx.encode('latin-1', 'xmlcharrefreplace') #to bytes
            path = os.path.join(self.dest, filename + ".ctx")
            with open(path, 'wb') as file:
                file.write(ctx)               

if __name__ == "__main__":
    supports_file = "support.publi"
    for filename in glob.glob("*.htm"):
        parse = parse_htm(filename)
        print("%s: found %d article(s)"%(filename, len(parse.content)))
        parse.get_supports(supports_file)
        print("%d unknown(s) source(s)" %len(parse.unknowns))
        for unknown in parse.unknowns:
            print ("unknown: %s" % unknown)
        parse.write_prospero_files()


