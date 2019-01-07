# -*- encoding: iso-8859-1 -*-
#----------------------------------------------------------
#Script de traitement des HTML xml issus d'Europresse pour Prospéro
#Génère les TXT et les CTX à partir des fichiers HTML du dossier
#version du 07/01/2019 par Josquin Debaz
#
# Author:      Guillaume Ollivier adapté de Factiva.py (Josquin Debaz)
#
# Created:     19/08/2011 adaptée pour Tirésias Desktop le 11/04/2012 par Josquin Debaz
# Copyright:   (c) gollivier 2011
#GNU General Public License
#Version 3, 29 June 2007
#See http://www.gnu.org/licenses/ or COPYING.txt for more information.
#-------------------------------------------------------------------------------
#!/usr/bin/env python


import os, glob, re,codecs
import HTMLParser


def ENCODE(UNICODE):

        #Des gremlins utf-8
        #http://www.eki.ee/letter/
        table = [
                ['&gt;','>'],
                ['&lt;','<'],
                ['<[bBiI]>',''],
                ['</[bBiI]>',''],
                ['«','"'],
                ['»','"'],
                ['&nbsp;',' '],
                ['&amp;','&'],
                ["<SUP>",""],
                ["</SUP>",""],
                [u"\u2009" , " " ],     #THIN SPACE
                [u"\u2018" , "'" ],     # LEFT SINGLE QUOTATION MARK
                [u"\u2019" , "'" ],     # RIGHT SINGLE QUOTATION MARK
                [u"\u20AC",'Euro'],
                [u'\u0152','Oe'],
                [u'\u0153','oe'],
                [u"\u2026",'...'],
                [u"\u201C",'"'],        # LEFT DOUBLE QUOTATION MARK
                [u"\u201D",'"'],        # RIGHT DOUBLE QUOTATION MARK
                [u"\u2013",'-'],        # EN DASH
                [u"\u2014",'-'],        # EM DASH
                [u"\u2022",'-'],        # BULLET
                [u"\u2020",'*'],        # DAGGER
                [u"\u2021",'**'],       # DOUBLE DAGGER
                [u"\u03c3",'d'],        #delta
                [u"\u03bc",'µ'],
                [u"\u201A",','],     # SINGLE LOW-9 QUOTATION MARK
                [u"\u0192",'f'],     # LATIN SMALL LETTER F WITH HOOK
                [u"\u201E",'"'],     # DOUBLE LOW-9 QUOTATION MARK
                [u"\u02C6",'^'],     # MODIFIER LETTER CIRCUMFLEX ACCENT
                [u"\u2030",'o/oo'],  # PER MILLE SIGN
                [u"\u0160",'S'],     # LATIN CAPITAL LETTER S WITH CARON
                [u"\u2039",'<'],     # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
                [u"\u017D",'Z'],     # LATIN CAPITAL LETTER Z WITH CARON
                [u"\u02DC",'~'],     # SMALL TILDE
                [u"\u2122",'TM'],    # TRADE MARK SIGN
                [u"\u0161",'S'],     # LATIN SMALL LETTER S WITH CARON
                [u"\u203A",'>'],     # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
                [u"\u017E",'Z'],     # LATIN SMALL LETTER Z WITH CARON
                [u"\u0178",'Y'],     # LATIN CAPITAL LETTER Y WITH DIAERESIS
                [u"\u222b","S"],     #Sigma
                [u'\u2212',"-"],
                [u'\u2420'," "],        #SYMBOL FOR SPACE
                [u'\u200A', ""],        #Hair space
                [u'\u1086',"O"],
                [u'\u1073',"d"],
                [u'\u1083',"P"],
                [u'\u1072',"a"],
                [u'\u1089',"c"],
                [u'\u1090',"T"],
                [u'\u2029'," "], #PARAGRAPH SEPARATOR
                [u'\u2500',"-"],
                [u"\u2028", "\n"], #LINE SEPARATOR
                [u"\u2759", " "], #MEDIUM VERTICAL BAR
                [u"\u2003", " " ], #EM SPACE
                [u"\u2010", "-"], #hyphenation
                [u"\u179C", "-"], #HEAVY ROUND-TIPPED RIGHTWARDS ARROW
                [u"\u2002", " "], #EN SPACE
                [u"\u25CF", "-"], #BLACK CIRCLE
                [u"\u25BA", "-"],
                [u"\u0300", "'"],
                [u"\u2192", "-"],
                [u"\u2680", "-"],
                [u"\u25A0", "-"],
                [u"\u0159", "r"],
                [u"\u0103", "a"],
                [u"\u0165", "u"],
                [u"\u015F", "s"],
                [u"\u017C", "z"],
                [u"\u0119", "e"],
                [u"\u0162", "T"],                  
                ]

        for T in table:
                UNICODE = re.sub(T[0],T[1],UNICODE)

        try:
                LATIN = UNICODE.encode('latin_1','strict')
        except:
                LATIN = UNICODE
##                print LATIN
##                LATIN = UNICODE.encode('latin_1','xmlcharrefreplace')
##                LOGS = open('log_gremlins.txt','a').write((re.search('.*&.*',LATIN).group(0) + "\n"))
        return LATIN

class supports(object):
        def __init__(self,cheminSupports):
                #récupère le support.publi
                self.supports = []
                self.supports_clefs = []
                fichier_supports = codecs.open(cheminSupports,'r',encoding='latin1').readlines()   #ouvre le fichier des supports
                for support in fichier_supports:
                        this_support = re.split('; ',support[:-1])
                        self.supports.append(this_support)
                        self.supports_clefs.append(this_support[0])
                
        def renseigne(self,source):
                try:
                        clef = self.supports_clefs.index(source)
                except ValueError:
                        print (["Un support inconnu : %s" % source])
                        #LOGS = open('log_inconnus.txt','a').write((source + "\n"))
                        return [u'INCONNU',source,u'INCONNU'] 
                else :
                        return self.supports[clef][1:]

class EcritFichiers(object):
        "Ecrit un fichier pour prospero."
        "En entrée la date jj/mm/aaaa et le radical prospérien"
        "L'appel à la fonction [ecrit] demande le contenu (en liste) et l'extention"
        "Cela créé les fichiers TXT et CTX sans doublons dans un dossier éponyme"

        def __init__(self,date,racine,dest):
                #instancie l'objet avec une date et une racine, lui donne son nom
                if (not os.path.isdir(dest)):
                        os.mkdir(dest)
                self.nom_fichier = self.nom_fichier_sans_doublon(date,racine,dest)

        def date_prosperienne(self,date):
                #la date de depart doit avoir la forme jj/mm/aaaa
                mois = ("1","2","3","4","5","6","7","8","9","A","B","C")   #les mois en tuple
                date = re.split('/',date)
                date = "%s%s%s" % (date[2][2:],mois[int(date[1])-1],date[0])
                return date

        def nom_fichier_sans_doublon(self,date,racine,dest):
                indice,base = "A", 64
                nom = "%s/%s%s%s" % (dest,racine,self.date_prosperienne(date),indice)
                while os.path.isfile(nom + ".txt"): #tant que le fichier existe
                        if  (ord(indice[-1]) < 90):
                                indice = chr(ord(indice[-1]) + 1) #incrémente le dernier caractère de l'indice
                        else :          #quand on arrive à Z
                                base += 1       #augmente la première lettre
                                indice = "A"    #remet la deuxième à A
                        if base > 64 : #à deux lettres
                                indice = chr(base) + indice
                        nom = "%s/%s%s%s" % (dest,racine,self.date_prosperienne(date),indice)
                return nom

        def fin_de_ligne (self,lignes):
                lignes = lignes
                lignes += "\n"
                return lignes

        def ecrit(self,contenu_fichier,extention):      #écrit le fichier, selon une liste de contenu et une extension
                nom_fichier = self.nom_fichier + extention      #ajoute l'extention
                pointeur_fichier = open(nom_fichier,'w')
                texte_fichier = map(self.fin_de_ligne,contenu_fichier)  #ajoute les fins de ligne
                pointeur_fichier.writelines(texte_fichier)      #écrit les lignes du fichiers
                pointeur_fichier.close()
                return nom_fichier

class parseEuropressHTML(object):
        "d'Europresse, au format html, aux fichiers de prospero"

        def __init__(self,fichier,support,dest):
                self.les_supports= supports(support)
                try:
                        self.dom = codecs.open(fichier, 'r',encoding='utf-8').read()
                except:
                        self.dom = codecs.open(fichier, 'r',encoding='ISO-8859-1').read()
                self.dest = dest
                self.listeFichiersecrits = []
                # repérage de tous les articles
                if re.search("<article>",self.dom):
                        self.articles = re.split("<article>",self.dom)
                        nb_art = len(self.articles) -1
                        cmp_art = 1                    #compteur d'article traités
                        for article in self.articles[1:]:
                                #print "Je traite l'article %d/%d du fichier %s" % (cmp_art, nb_art, fichier)
                                if re.search('<span class="DocPublicationName">(Rapports|Reports) -', article): 
                                    print "je passe l'extrait de rapport", re.search('<span class="DocPublicationName">(Rapports|Reports) - .*</span>  <span class="DocPublicationName">', article).group(0)
                                else:
                                    if re.search('<div class="twitter">', article):
                                        print "je passe le tweet"
                                    else:
                                        self.analyse_new(article)
                                cmp_art += 1
                                
                        

                else :
                        self.dom= self.dom.replace('\n', ' ')
                        self.articles = self.dom.split("<br><br><br><table")
                        nb_art = len(self.articles) -1
                        cmp_art = 1                    #compteur d'article traités
                        for article in self.articles[:-1]:  # supprime de la liste le dernier enregistrement
                                ##print "Je traite l'article %d/%d du fichier %s" % (cmp_art, nb_art, fichier)
                                self.analyse(article)
                                cmp_art += 1

        def recup_content_class(self,classe,texte):
                balise = re.findall("<(\w*) class=\"%s\">"% classe,texte) [0]
                texte = re.split("<%s class=\"%s\">" % (balise,classe),texte) [1]
                texte = re.split("</%s>"%balise,texte)[0]
                texte = re.sub("\s*$","",texte)
                return texte

        def analyse_new(self,article):
                #récupère les données pour le ctx
                contenu_ctx = ["fileCtx0005","titre","support","","","date","","type support inconnu", "","", "","","","n","n",""]

                journal = self.recup_content_class("DocPublicationName",article)

                if re.search("<", journal) : # gestion de cas particuliers
                    journal = re.split("<", journal)[0]
                if re.search(", no", journal):
                    journal = re.split(", ", journal)[0]
                h = HTMLParser.HTMLParser()
                journal =  h.unescape(journal)
                contenu_ctx[2] = self.nettoie_htm(journal)

                date = self.recup_content_class("DocHeader", article)
##                print date
                if re.search("\d{1,} \S* \d{4} -",date):
                        date = re.search("(\d{1,} \S* \d{4})",date).group(1)
                elif re.search(u"\w* \d{1,}, \d{4}", article):
                        date = re.search(u"(\w* \d{1,}, \d{4})", article).group(1)
                else:
                        print "pb date"
                date = h.unescape(date)
                contenu_ctx[5] = self.trait_date(date)
                #print contenu_ctx[5]
                    
                        
                try:
                    titre = self.recup_content_class("titreArticleVisu rdp__articletitle",article)
                except:
                    titre = self.recup_content_class("titreArticleVisu",article)
                contenu_ctx[1] = self.nettoie_htm(titre) 

                try:
                    corps = self.recup_content_class("DocText",article)
                except:
                    corps = self.recup_content_class("DocText clearfix",
                    article)
                    
                corps = self.nettoie_htm(corps)
                contenu_txt = [contenu_ctx[1],'.']  #on commence par le titre
                contenu_txt.append(corps)


 
                #gère le support
                support = self.les_supports.renseigne(contenu_ctx[2])
                RACINE = re.sub('\r',"",support[2])
                if (support[0] != 'INCONNU'):
                        contenu_ctx[2] = contenu_ctx[6] = support[0]    #le journal
                        contenu_ctx[7] = ENCODE(support[1])                     #type support


                #écrit les fichiers ctx et txt
                les_fichiers = EcritFichiers(ENCODE(contenu_ctx[5]),RACINE,self.dest)
                try :
                        contenu_ctx = map(ENCODE,contenu_ctx)
                        self.listeFichiersecrits.append(les_fichiers.ecrit(map(self.enleve_sauts_de_lignes,contenu_ctx),".ctx"))
                except :
                        print ("probleme CTX ") + str(contenu_ctx)
                try :
                        self.listeFichiersecrits.append(les_fichiers.ecrit(map(ENCODE,contenu_txt),".txt"))
                except :
                        print ("probleme TXT" )#+ str(contenu_ctx)




        def analyse(self,article):
                #récupère les données pour le ctx
                contenu_ctx = ["fileCtx0005","titre","support","","","date","","type support inconnu", "","", "","","","n","n",""]
                ##print article

                journal = re.findall("<span class=\"DocPublicationName\">(.*)<\/span><br><span class=\"Doc", article)[0]    #le journal  <span class="DocPublicationName">La Voix du Nord</span><br><span class="DocPublicationName">
                if re.search("<", journal) : # gestion de cas particuliers
                    journal = re.split("<", journal)[0]

                if re.search(", no", journal):
                    journal = re.split(", ", journal)[0]

##                print journal
                
                contenu_ctx[2] = self.nettoie_htm(journal)

                if re.search(u"<span class=\"DocHeader\">(\d{1,} \S* \d{4})</span>", article):
                        date = re.search(u"<span class=\"DocHeader\">(\d{1,} \S* \d{4})</span>", article).group(1)
                elif re.search(u"<span class=\"DocHeader\">(\S* \d{4})</span>", article):
                        date = re.search(u"<span class=\"DocHeader\">(\S* \d{4})</span>", article).group(1)
                elif re.search(u"<span class=\"DocHeader\">(\S* \d{1,}, \d{4})</span>", article):
                        date = re.search(u"<span class=\"DocHeader\">(\S* \d{1,}, \d{4})</span>", article).group(1)
                        

##                try :
##                    date = re.findall()[0] #la date  <span class="DocHeader">14 octobre 2010</span><span class="DocHeader">
##                except :
##                    date = re.findall("<span class=\"DocHeader\">((.*) \d{4})</span>", article)[0][0] #la date  <span class="DocHeader">14 octobre 2010</span><span class="DocHeader">
                contenu_ctx[5] = self.trait_date(date)

                #récupère les données pour le txt
                try :
                        txt = re.findall("<span class=\"TitreArticleVisu\">(.*)<p></p><b><i>" , article)[0]
                except:
                        txt = re.findall("<span class=\"TitreArticleVisu\">(.*)</p>© ",article)[0]

                #print txt
                
                #try:
                frag_txt = re.split("</span><br>", txt) #</span><br><br>
                #print len(frag_txt)
                contenu_ctx[1] = self.nettoie_htm(frag_txt[0]) # titre
                
                if len(frag_txt) == 2 :
                    corps = self.nettoie_htm(frag_txt[1])
                #    print corps
                elif len(frag_txt) == 3:
                    corps = self.nettoie_htm(frag_txt[1]) +'\n' + self.nettoie_htm(frag_txt[2])
                #    print corps
                else :
                    print ('erreur')

                contenu_txt = [contenu_ctx[1],'.']  #on commence par le titre
                contenu_txt.append(corps)

                
                #gère le support
                support = self.les_supports.renseigne(contenu_ctx[2])
                RACINE = re.sub('\r',"",support[2])
                if (support[0] != 'INCONNU'):
                        contenu_ctx[2] = contenu_ctx[6] = support[0]    #le journal
                        contenu_ctx[7] = ENCODE(support[1])                     #type support

##                print (contenu_ctx)
##                print (contenu_txt)
                
                #écrit les fichiers ctx et txt
                les_fichiers = EcritFichiers(ENCODE(contenu_ctx[5]),RACINE,self.dest)
                try :
                        contenu_ctx = map(ENCODE,contenu_ctx)
                        self.listeFichiersecrits.append(les_fichiers.ecrit(map(self.enleve_sauts_de_lignes,contenu_ctx),".ctx"))
                except :
                        print ("probleme CTX ") + str(contenu_ctx)
                try :
                        self.listeFichiersecrits.append(les_fichiers.ecrit(map(ENCODE,contenu_txt),".txt"))
                except :
                        print ("probleme TXT" )#+ str(contenu_ctx)

        def trait_date(self, d):
##            print d
            dic_mois = {'janvier': '01', 'Janvier': '01', u'février': '02', u'Février': '02', 'mars': '03', 'Mars' : '03', 'avril': '04', 'mai': '05', 'Mai': '05',
                        'juin': '06', 'juillet': '07', 'Juillet': '07', 'aout': '08', u'août': '08', 'septembre': '09', 'octobre': '10',
                        'novembre': '11', u'décembre': '12', 'January' : '01', 'February' : '02', 'March' : '03', 'April' :'04', 'May': '05',
                        'June' : '06', 'July' : '07', 'August' : '08', 'September' : '09', 'October' : '10', 'November' : '11', 'December' : '12',
                        }
            d = d.replace('  ', ' ')
            d = self.nettoie_htm(d)
            d = re.sub(',','',d)
            frag = d.split(' ')
##            print len(frag), frag

            if len(frag) == 3 :
                try:
                        mois = dic_mois[frag[1]]
                        jour = "%02d" %  int(frag[0])
                except :
                        mois = dic_mois[frag[0]]
                        jour = "%02d" % int(frag[1])
                date = "%s/%s/%s" % (jour,mois,frag[2])


            elif len(frag)== 2 :
                mois = dic_mois[frag[0]]
                date = '01/'+ mois +'/'+ frag[1]
            elif len(frag) == 4:
                mois = dic_mois[frag[1]]
                date = frag[2] +'/'+ mois +'/'+ frag[3]
            else :
                print ("traitement de date échoué")

##            print date
            return date


        def nettoie_htm(self, html):
            html = html.replace("&amp;", "&")
            html = html.replace('<p></p>', " ")
            html = html.replace('<br>', "\n")
            # ne prend pas en compte les texte entre < et > soit ce qui n'est pas une balise html !!
            inside = 0
            text = ''
            for char in html:
                if char == '<':
                    inside = 1
                    continue
                elif (inside == 1 and char == '>'):
                    inside = 0
                    continue
                elif inside == 1:
                    continue
                else:
                    text += char
            text = text.replace('">\t', "")
            text = text.replace('\r\n', " ")
            text = text.replace(' \t', "\n")
            text = re.sub('[ ]{1,}', " ", text)
            text = text.replace('&gt;', "")
            text = re.sub('^\s*','',text) #les blancs au début
            text = re.sub('\s*$','',text) #les blancs à la fin
            text = re.sub('\s',' ',text)

            return text

        def enleve_sauts_de_lignes(self,data):
                return re.sub('\s',' ',data)




## PROCEDURE PRINCIPALE

if __name__ == "__main__":        
        LISTE =  glob.glob("*.htm*")
        cmp_fich = 1
        for fichier in LISTE:
                print ("Je traite %s, fichier %d sur %d\n" % (fichier,cmp_fich,len(LISTE)))
                traite = parseEuropressHTML(fichier,"support.publi",".")
                cmp_fich +=1
                print ("J'ai créé les fichiers : %s " % traite.listeFichiersecrits )
        print( "Traitement fini !!")
                
        
      






