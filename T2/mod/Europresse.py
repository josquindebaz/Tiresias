import glob
import re
import html
import os
import datetime

try:
    import cleaning
    from supports import publi
except:
    from mod.cleaning import cleaner
    from mod.supports import publi

 
class parse_html(object):
    def __init__(self, f):
        with open(f, 'rb') as p:
            b = p.read().decode('utf-8')
        self.articles = re.split('<article>', b)[1:]
        self.parsed_articles = []
        for a in self.articles:
            art = self.parse_article(a)
            if art:
                self.parsed_articles.append(art)

    def parse_article(self, a):
        if re.search('<p class="link-not-hosted">', a):
            #print("only a link")
            return False
        elif re.search('class="DocPublicationName">(Rapports|Reports) -', a):
            #print("only a report extract")
            return False
        elif re.search('<div class="twitter">', a):
            #print("only a tweet")
            return False            
        else:
            a =  html.unescape(a)
            #split header and article
            h, art = re.split('</header>', a)

            #get header infos
            pubname = self.in_tag(h, "DocPublicationName")
            pubname = self.form_support(pubname)            
            date = self.in_tag(h, "DocHeader")
            date = self.get_date(date)
            title = self.in_tag(h, "titreArticle")
            title = self.strip_tags(title)
            narrator = self.in_tag(h, "docAuthors")
            m_subtitle = re.compile("<b><p>(.*)</p></b>")
            if m_subtitle.search(h):
                subtitle = m_subtitle.search(h).group(1)
            else:
                subtitle = False

            #get text
            text = self.in_tag(a, "docOcurrContainer")
            text = self.strip_tags(text)

            return {
                "source": pubname,
                "date": date,
                "title": title,
                "narrator": narrator,
                "subtitle": subtitle,
                "text": text
                }

    def form_support(self, s):
        m = re.compile("\s*(<|\(|,).*$")
        n = m.sub('', s)
        return n    

    def strip_tags(self, c):
        m = re.compile('(<(\S{1,}) class=(.))')
        while(m.search(c)):
            s = m.split(c, 1)
            t = re.split("%s>"%s[3], s[4], 1)[1]
            t = re.sub("</%s>"%s[2], "", t, 1)
            c = s[0] + t
        c = re.sub("</*mark>", "", c)
        return c
        
        
    def get_date(self, d):
        m = re.compile("(\d{1}) (\S*) (\d{4})")
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
        if m.search(d):
            day, month, year = m.search(d).group(1, 2, 3)
            if month not in months:
                print("I don't know this month %s" %month)
                return False
            else:
                month = months[month]
            return "%s/%s/%s" %("%02d" % int(day), month, year)
        else:
            print("Problem reading date")
            return False
            
    def in_tag(self, html, tag):
        m = re.compile('(<(\S*) \S*=[\'"]%s[\'"]>)'%tag)
        if m.search(html):
            s = m.split(html)
            if len(s) == 4:
                closing = re.split("</%s>"%s[2], s[3], 1)
                if len(closing) == 2:
                    return closing[0].strip()
                else:
                    print("Can't find closing %s"%s[2])
                    return False
            else:
                print("pb s size")
                return False
        else:
            #print("Can't find tag %s"%tag)
            return False

class Process_article(object):
    def __init__(self, a, dest, c=1):
        self.dest = dest
        s = publi()
        if a['source'] not in s.codex.keys():
            prefix = "EUROPRESSE"
            source = a['source']
            source_type = "unknown source"
        else:
            prefix = s.codex[a['source']]['abr']
            source = s.codex[a['source']]['source']
            source_type = s.codex[a['source']]['type']

        self.filename = self.file_name(a['date'], prefix)

        text = a['title'] + "\r\n.\r\n"
        text += a['subtitle'] + "\r\n.\r\n" if a['subtitle'] else ""
        text += a['text']
        
        ctx = [
            "fileCtx0005",
            a['title'],
            source,
            "","",
            a['date'],
            "",
            source_type,
            "", "", "",
            "Processed by Tiresias on %s"\
                % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "", "n","n", ""
            ]
        ctx = "\r\n".join(ctx)

        if (c):
            cl_txt = cleaner(text.encode('utf-8'))
            text = cl_txt.content.encode('latin-1', 'xmlcharrefreplace') #to bytes
            cl_ctx = cleaner(ctx.encode('utf-8'))
            ctx = cl_ctx.content.encode('latin-1', 'xmlcharrefreplace') #to bytes    
        else:
            ctx = ctx.encode('latin-1', 'xmlcharrefreplace') #to bytes
            text = text.encode('latin-1', 'xmlcharrefreplace') #to bytes
        
        path = os.path.join(self.dest, self.filename + ".txt")
        with open(path, 'wb') as f:
            f.write(text)
                 
        path = os.path.join(self.dest, self.filename + ".ctx")
        with open(path, 'wb') as f:
            f.write(ctx)
        
            
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

if __name__ == "__main__":
    for f in glob.glob("*.htm*"):
        p = parse_html(f)
    for a in p.parsed_articles:
        Process_article(a, "test")
        #pass
    
        
