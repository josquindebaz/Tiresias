# -*- coding: utf-8 -*-
# Author Josquin Debaz
# GPL 3

import datetime
import os
import re
import ssl
import time
import urllib.parse
import urllib.request

from mod.AssembleeParser import AssembleeParser

ssl._create_default_https_context = ssl._create_unverified_context

VERBOSE = 0


class QuestionParlementaire(object):
    def __init__(self, url):
        self.final = None
        self.D = None
        self.url = url

    def retrieve(self):
        with urllib.request.urlopen(self.url) as page:
            charset = page.info().get_param('charset')

            if charset:
                buf = page.read().decode(charset)
            else:
                p = page.read()
                buf = p.decode("latin-1")

                # search for misencoding
                if re.search('encoding="UTF-8', buf):
                    buf = p.decode("utf-8")

            if re.search("questions.assemblee-nationale.fr", self.url):
                self.D = AssembleeParser(buf).data
            else:
                self.D = ParseSenat(buf).data

    def ctx_content(self, r, title, ref):
        c = ["fileCtx0005", title]
        # title
        # author
        if r:
            c.append(self.D['ministere'])
        else:
            c.append(self.D['aut'])
        # group
        if r:
            c.append("")
        else:
            c.append(self.D['groupe'])
        # dest
        if r:
            c.append(self.D['aut'])
        else:
            c.append(self.D['ministere'])
        # date
        if r:
            c.append(self.D['dpr'])
        else:
            c.append(self.D['dpq'])
        # journal
        c.append(self.D['support'])
        # type
        if r:
            c.append("Réponse à une %s" % self.D['nature'])
        else:
            c.append(self.D['nature'])
        # reponse ?
        if r:
            c.append("")
        else:
            c.append(self.D['ASREP'])
        # status
        if r:
            c.append("Ministère")
        else:
            c.append("Parlementaires")
        # loc
        if r:
            c.append("")
        else:
            c.append(self.D['dept'])
        # CL1
        c.append("Retrieved on {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        # tail
        c.extend(["", "n", "n", "REF_HEURE:00:00"])

        try:
            c = list(map(lambda x: re.sub(r'\s+', ' ', x), c))
        except:
            if VERBOSE:
                print("pb ctx list", c)

        # source
        c.append("REF_EXT:%s" % self.D['source'])
        # link between question and answer
        if r:
            c.append(fr"REF_EXT:{self.final}\{ref}")
        elif self.D['ASREP'] == "Avec réponse":
            c.append(fr"REF_EXT:{self.final}\{ref}")
        return c

    def process(self, source=None, dest=None, temp=None):
        if not source:
            self.D['source'] = self.url
        else:
            self.D['source'] = source
        if not dest:
            self.final = os.getcwd()
        else:
            self.final = dest
        if not temp:
            cible = self.final
        else:
            cible = temp

        filenames = []

        natures = {
            'Question écrite': 'QE',
            'Question au Gouvernement': 'QG',
            'Question orale sans débat': 'QOSD',
            'Question orale avec débat': 'QOAD',
            'Question orale': 'QO',
            "Question d'actualité au gouvernement": 'QG'
        }

        try:
            nat = natures[self.D['nature']]
        except:
            print("nature unknown: %s" % self.D['nature'])
            nat = "NU"

        txt_writer = WriteFile(nat, self.D['leg'], self.D['num'], 'txt')

        subtitle = "%s %s, publiée au JO le %s" \
                   % (self.D['nature'], self.D['num'], self.D['dpq'])
        if self.D['pgq']:
            subtitle += " (page %s)" % self.D['pgq']

        lines = [
            self.D['title'],
            ".",
            subtitle,
            ".", "",
            self.D['question']
        ]

        filenames.append(txt_writer.w(cible, lines))

        ctx_writer = WriteFile(nat, self.D['leg'], self.D['num'], 'ctx')
        q_ctx = self.ctx_content(0, self.D['title'], txt_writer.nom_rep)
        filenames.append(ctx_writer.w(cible, q_ctx))

        if self.D['ASREP'] == "Avec réponse":
            r_title = "Réponse à la %s %s, publiée au JO le %s (page %s)" \
                      % (self.D['nature'], self.D['num'],
                         self.D['dpr'], self.D['pgr'])
            txt_rep = [
                r_title,
                ".",
                "",
                self.D['reponse']
            ]

            filenames.append(txt_writer.w(cible, txt_rep, 1))

            r_ctx = self.ctx_content(1, r_title, txt_writer.nom_fichier)
            filenames.append(ctx_writer.w(cible, r_ctx, 1))


class WriteFile(object):
    """Write a QP for Prospero"""

    def __init__(self, nature, leg, num, extension):
        # nom de fichier complété par des zéros au besoin
        nom_court = "%s_%s_%s" % (nature, leg, '0' * (6 - len(num)) + num)
        self.nom_fichier = "%s.%s" % (nom_court, extension)
        self.nom_rep = "%sREP.%s" % (nom_court, extension)

    def fin_de_ligne(self, ligne):
        ligne += "\r\n"
        try:
            return ligne.encode('latin1', errors='xmlcharrefreplace')
        except:
            return ligne

    def w(self, cible, contenu_fichier, rep=0):
        if rep == 1:
            nom = self.nom_rep
        else:
            nom = self.nom_fichier
        texte_fichier = list(map(self.fin_de_ligne, contenu_fichier))

        with open(os.path.join(cible, nom), 'wb') as p:
            p.writelines(texte_fichier)

        return nom


class CrawlAss(object):
    """Search in Assemblée db via website form"""

    def __init__(self, leg, words):
        self.dicQ = {}
        html = self.get_assemblee_request(leg, words)
        self.get_questions(html)
        if VERBOSE:
            print("found %d questions" % len(self.dicQ))

    def get_assemblee_request(self, leg, words):
        # !7th legislature has only empty data
        # !lack of accentuation before 11th
        url = "http://www2.assemblee-nationale.fr/recherche/resultats_questions/index.asp?legislature"
        form_data = (
            ('legislature', leg),
            ('q', words),
            ('q_in', 0),
            ("limit", 10000000),
        )
        data = urllib.parse.urlencode(form_data).encode()
        with urllib.request.urlopen(url, data) as response:
            return response.read().decode()

    def get_questions(self, html):
        for q in re.split('<tr>', html)[2:]:
            m = re.compile(r'questions\.assemblee-nationale.fr/(.*).htm"><strong>.* - (.*)</strong>')
            lk, num = m.search(q).group(1, 2)
            m = re.compile(r'<td class="text-center">\s*<strong>\S* (.*)</strong>')
            nom = m.search(q).group(1)
            m = re.compile(r'au JO le\s*<strong>(\d{2}/\d{2}/\d{4})</strong>')
            date = m.search(q).group(1)
            title = re.search('<em>(.*)</em>', q).group(1)
            response = True if re.search('Réponse JO le', q) else False

            self.dicQ[lk] = {'title': title,
                             'number': num,
                             'depute': nom,
                             'date': date,
                             'response': response,
                             'url': self.create_url(lk)}

    def create_url(self, q):
        return "http://questions.assemblee-nationale.fr/%s.htm" % q


class ParseSenat(object):
    def __init__(self, html):
        d = {'title': self.get_title(html), 'leg': self.get_leg(html)}

        spl = re.split("<h2>", html)
        q = spl[1]
        d['num'] = self.get_num(q)
        d['aut'] = self.get_aut(q)
        d['dept'], g = self.get_from(q)
        d['groupe'] = self.find_groupe(g)
        d['nature'] = self.get_nature(q)

        d['dpq'], d['pgq'] = self.get_publication(q)
        d['support'] = "Journal officiel du Sénat"

        content = re.split('<p align="justify">', q)
        d['question'] = self.formate_txt(content[1])

        if len(spl) > 2:
            d['ASREP'] = "Avec réponse"
            rep = spl[2]
            d['ministere'] = self.get_ministere(rep)
            d['dpr'], d['pgr'] = self.get_publication(rep)
            rep_content = re.split('<p align="justify">', rep)
            d['reponse'] = self.formate_txt(rep_content[1])
        else:
            d['ASREP'] = "Sans réponse"
            d['ministere'] = ""

        self.data = d

    def formate_txt(self, txt):
        return re.sub(r'<br/>\s*', '\n',
                      re.split('</p>', txt)[0]
                      ).strip()

    def get_title(self, b):
        m = re.compile(r'<h1.*\r\n\s*(.*)\s*\r\n')
        if m.search(b):
            return m.search(b).group(1).strip()
        else:
            return False

    def get_leg(self, b):
        m = re.compile(r'(\d*)\s*<sup>\S*</sup> l&eacute;gislature')
        if m.search(b):
            return m.search(b).group(1)
        else:
            return False

    def get_num(self, b):
        m = re.compile(r'n&deg;\s*(.*)\r')
        if m.search(b):
            return m.search(b).group(1)
        else:
            return False

    def get_aut(self, b):
        m = re.compile(r'de\s*<b>\s*.*\s*.* M.*\s*(.*)\r')
        if m.search(b):
            return re.sub(r"\s+", " ", m.search(b).group(1)).strip()
        else:
            return False

    def get_from(self, b):
        m = re.compile(r'(</b>|<span class="rouge">)\s*\((.*) - (.*)\)')
        if m.search(b):
            return m.search(b).group(2, 3)
        else:
            return False, False

    def get_nature(self, b):
        m = re.compile(r'\s*(.*\S)\s*n&deg;')
        if m.search(b):
            return re.sub("(&#39;|&quot;)", "'", m.search(b).group(1))
        else:
            return False

    def get_publication(self, b):
        m1 = re.compile(r'dans le JO S&eacute;nat du\s*([\d/]*)\s*')

        if m1.search(b):
            date = m1.search(b).group(1)
        else:
            date = False

        m2 = re.compile(r'- page\s*(\d*)')

        if m2.search(b):
            page = m2.search(b).group(1)
        else:
            page = False

        return date, page

    def get_ministere(self, b):
        m = re.compile(r'Réponse du (.*)\s*')
        if m.search(b):
            minis = m.search(b).group(1).strip()
            minis = re.sub("ministère :", "Ministère de", minis)
            return minis
        else:
            return False

    def find_groupe(self, g):
        groupes = {
            "CRC": "Groupe Communiste Républicain et Citoyen",
            "CRCE": "Groupe Communiste, Républicain, Citoyen et Écologiste",
            "CRCE-R": "Groupe Communiste, Républicain, Citoyen et Écologiste",
            "CRC-SPG": "Groupe Communiste Républicain, Citoyen et des \
sénateurs du Parti de Gauche",
            "SOC": "Groupe Socialiste",
            "SOCR": 'Groupe Socialiste et républicain',
            "SOC-R": 'Groupe Socialiste et républicain',
            "SOCR-A": 'Groupe Socialiste et républicain',
            "Socialiste et républicain": 'Groupe Socialiste et républicain',
            "SOC-A": "Groupe socialiste et apparentés",
            "UC": "Groupe Union centriste - UDF",
            "UC-UDF": "Groupe Union centriste - UDF",
            "RDSE": "Groupe du Rassemblement Démocratique et Social Européen",
            "RDSE-R": "Groupe du Rassemblement Démocratique et Social Européen",
            "UMP": "Groupe Union pour un Mouvement Populaire",
            "NI": "Réunion administrative des Sénateurs ne figurant \
sur la liste d'aucun groupe",
            "RI": "Groupe des Républicains Indépendants",
            "RPR": "Groupe du Rassemblement pour la République",
            "Les Républicains": "Groupe Les Républicains",
            "Les Républicains-A": "Groupe Les Républicains",
            "Les Républicains-R": "Groupe Les Républicains",
            "CRARS": "Centre Républicain d'Action Rurale et Sociale",
            "COM": "Groupe Communiste",
            "C": "Groupe Communiste",
            "Communiste républicain et citoyen":
                "Groupe Communiste républicain et citoyen",
            "GD": "Groupe de la Gauche Démocratique",
            "G.D.": "Groupe de la Gauche Démocratique",
            "RDE": "Groupe du Rassemblement Démocratique Européen",
            "R.D.E.": "Groupe du Rassemblement Démocratique Européen",
            "RIAS": "Groupe des Républicains Indépendants d'Action Sociale",
            "UCDP": "Groupe de l'Union Centriste des Démocrates de Progrès",
            "UDI-UC": "Groupe UDI - Union centriste",
            "U.R.E.I.":
                "Groupe de l'Union des Républicains et des Indépendants",
            "U.C.D.P.":
                "Groupe de l'Union Centriste des Démocrates de Progrès",
            "ECOLO": "Groupe écologiste",
            "UCR": "Union centriste et républicaine",
            "UC-R": "Union centriste et républicaine",
            "LaREM": "La République en Marche",
            "Les Indépendants": "Groupe Les Indépendants",
        }
        if g in groupes.keys():
            return groupes[g]
        else:
            print("unknown group", g)
            return g


class CrawlSenat(object):
    """Search in Senat db via website form"""

    def __init__(self, words, date_from, date_to):
        words = words.split(" ")
        # search after 2 avril 1978.
        # Not digitized before 8th legislation (may 86)

        if (time.strptime(date_from,
                          "%d/%m/%Y") < time.strptime("02/04/1978", "%d/%m/%Y")):
            date_from = "02/04/1978"

        html = self.getpage(words, date_from, date_to)
        if html:
            self.dicQ = {}
            if re.search("Il n'y a aucun résultat pour cette recherche.", html):
                self.n = 0
            else:
                self.n = int(re.search(r'results-number-global">\s*(\d*)\s*', html).group(1))
                self.retrieve_question(html)
                for offset in range(10, self.n, 10):
                    html = self.getpage(words, date_from, date_to, offset)
                    self.retrieve_question(html)
            if VERBOSE:
                print("found %d questions" % len(self.dicQ))
        else:
            if VERBOSE:
                print("pb getpage")
            self.dicQ = {}

    def getpage(self, words, date_from, date_to, offset=0):
        words = [urllib.parse.quote(w) for w in words]
        url = "https://www.senat.fr/basile/rechercheQuestion.do?tri=da\
&radio=deau&rch=qs&aff=ens\
&unk=%s&de=%s&au=%s&off=%d" % ("+".join(words), date_from, date_to, offset)
        urllib.request.urlopen(url)

        try:
            if VERBOSE:
                print(url)
            with urllib.request.urlopen(url) as page:
                charset = page.info().get_param('charset')
                if charset:
                    buf = page.read().decode(charset)
                else:
                    buf = page.read().decode("latin1")
            return buf
        except:
            return False

        # aff=ens afficher ensemble avec et sans réponse (sep sinon)
        # off = 0 = page 1 ; 10 = page 2
        # rch=qs question simple
        # de date départ yyyymmjj
        # au date arrivée yyyymmjj
        # radio=deau
        # tri : p pertinence, dd date descendante, da date ascendante
        # _c=MC1+MC2

    def retrieve_question(self, html):
        m1 = re.compile(r'visio.do\?id=(.*)&amp;idtable=.*\r\n\s*(.*)\r\n')
        m2 = re.compile(r'Question n&deg; (\S*)')
        m3 = re.compile(r'posée par\s*.*((\s*.*){2})')
        m4 = re.compile(r"\d{2}/\d{2}/\d{4}")

        for q in re.split(r'<div class="document document-\d*"', html)[1:]:
            lk, title = m1.search(q, re.S).group(1, 2)
            title = re.sub("(&#39;|&quot;)", "'", title)
            if re.search("&", title):
                if VERBOSE:
                    print("&", title)
            num = m2.search(q).group(1)
            if m3.search(q, re.S):
                nom = re.sub(r"\s+", " ", m3.search(q, re.S).group(1)).strip()
            else:
                nom = "error"
            date = m4.search(q).group(0)
            r = True if re.search(r'Réponse\s*.*', q) else False
            self.dicQ[lk] = {'title': title,
                             'number': num,
                             'senator': nom,
                             'date': date,
                             'response': r,
                             'url': self.create_url(lk)}

    def create_url(self, q):
        return "https://www.senat.fr/basile/visio.do?id=%s" % q


if __name__ == '__main__':
    test = CrawlAss(13, '"ronds points"')
    for q in test.dicQ.keys():
        t = QuestionParlementaire(test.create_url(q))
        t.retrieve()
        t.process()
