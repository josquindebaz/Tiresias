# -*- encoding: iso-8859-1 -*-
#----------------------------------------------------------
#Script de traitement de xml issus de FACTIVA pour Prospéro
#Génère les TXT et les CTX à partir des fichiers  HTM du dossier
#version du 13 janvier 2010 + gremlins  2010-2011-2012
#18 février 2012 ajout des fichier HTM
#31 octobre 2012 fonctionnement sur plusieurs version de factiva
#Josquin Debaz
#GNU General Public License
#Version 3, 29 June 2007
#See http://www.gnu.org/licenses/ or COPYING.txt for more information.
#----------------------------------------------------------

from xml.dom import minidom
import re,os,glob,codecs



def enleve_sauts_de_lignes(data):
        return re.sub('\s',' ',data)

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

        try: LATIN = UNICODE.encode('latin_1','strict')
        except:
                LATIN = UNICODE.encode('latin_1','xmlcharrefreplace')
                LOGS = open('log_gremlins.txt','a').write((re.search('.*&.*',LATIN).group(0) + "\n"))
        LATIN = re.sub('<span class="companylink">','',LATIN)
        LATIN = re.sub('</span>','',LATIN)
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
                        #LOGS = open('log_inconnus.txt','a').write((source + "\n"))
                        #print ("Un support inconnu : %s" % source)
                        return [u'INCONNU',source,u'INCONNU'] 
                else :
                        return self.supports[clef][1:]
                
class EcritFichiers(object):
        "Ecrit un fichier pour prospero."
        "En entrée la date jj/mm/aaaa et le radical prospérien"
        "L'appel à la fonction [ecrit] demande le contenu (en liste) et l'extention"
        "Cela créé les fichiers TXT et CTX sans doublons dans un dossier éponyme"

        def __init__(self,date,racine,rep):
                self.rep = rep
                #instancie l'objet avec une date et une racine, lui donne son nom
                self.nom_fichier = self.nom_fichier_sans_doublon(date,racine)
                

        def date_prosperienne(self,date):
                #la date de depart doit avoir la forme jj/mm/aaaa
                mois = ("1","2","3","4","5","6","7","8","9","A","B","C")   #les mois en tuple
                date = re.split('/',date)
                date = "%s%s%s" % (date[2][2:],mois[int(date[1])-1],date[0])
                return date 

        def nom_fichier_sans_doublon(self,date,racine):
                indice,base = "A", 64
                nom = "%s%s%s" % (racine,self.date_prosperienne(date),indice)
                while os.path.isfile(os.path.join(self.rep,nom + ".txt")): #tant que le fichier existe
                        if  (ord(indice[-1]) < 90):
                                indice = chr(ord(indice[-1]) + 1) #incrémente le dernier caractère de l'indice
                        else :          #quand on arrive à Z
                                base += 1       #augmente la première lettre
                                indice = "A"    #remet la deuxième à A
                        if base > 64 : #à deux lettres 
                                indice = chr(base) + indice
                        nom = "%s%s%s" % (racine,self.date_prosperienne(date),indice)
                return nom

        def fin_de_ligne (self,lignes):
                lignes = lignes
                lignes += "\n"
                return lignes

        def ecrit(self,contenu_fichier,extention):      #écrit le fichier, selon une liste de contenu et une extension
                nom_fichier = self.nom_fichier + extention      #ajoute l'extention
                pointeur_fichier = open(os.path.join(self.rep,nom_fichier),'w')
                texte_fichier = map(self.fin_de_ligne,contenu_fichier)  #ajoute les fins de ligne
                pointeur_fichier.writelines(texte_fichier)      #écrit les lignes du fichiers
                pointeur_fichier.close()
                return nom_fichier



class parsefactivahtm(object):
        "de factiva, au format htm, aux fichiers de prospero"
        def __init__(self,fichier,fichier_supports):
                self.buf = codecs.open(fichier,'r',encoding='utf-8',errors='strict').read()
                liste_supports = []
                self.pb_support = 0
                articles = re.split(' class="article [a-z]{2}Article">',self.buf)[1:]
                for article in articles:
                        support = 0
                        s = re.split('<div>',article)
                        for t in s:
                                if re.search("\d{1,2} [a-zéèûñíáóúüãçA-Z]* \d{4}</div>",t):
                                        if re.search("\d{2}:\d{2}</div>", s[s.index(t)+1]):
                                                support = s[s.index(t)+2][:-6]
                                        else :
                                                support = s[s.index(t)+1][:-6]
                        if not (support) :
                                try :
                                        support = self.recup(article,'<b>SN</b>&nbsp;</td><td>','</td>')
                                except :
                                        self.pb_support += 1
                                        
                        if (support) :
                                liste_supports.append(support )
                                
                self.Narticles = len(articles)
                self.liste_inconnus = []
                self.les_supports = supports(fichier_supports)
                for support in list(set(liste_supports)):
                        if self.les_supports.renseigne(support)[0] == 'INCONNU':
                                self.liste_inconnus.append(support)

        def traite(self,rep):
                self.rep = rep
                #L = re.split('\n\*AN\*\s*\n',self.buf)[:-1]
                L = re.split(' class="article [a-z]{2}Article">',self.buf)[1:]
                self.fichiers_generes = 0
                listeTXT = []
                for article in L:
                        listeTXT.append(self.analyse(article))
                return listeTXT

        def recup(self,texte,balisedebut,balisefin):
                #print re.search(balisedebut,texte), texte
                recup = re.split(balisedebut,texte,1)[1]
                recup = re.split(balisefin,recup,1)[0]
                return recup

        def analyse(self,article):
##                print (article)
                #récupère les données pour le ctx
                contenu_ctx = ["fileCtx0005","titre","support","","","date","","type support", "","", "","","","n","n",""]
                
                #titre
                try :
			marque =  re.search('<(b|span) class=["\'][a-z]{2}Headline',article).group(1)
                        title = self.recup(article,'<%s class=["\'][a-z]{2}Headline["\']>'%marque,'</%s>'%marque)
                        title = re.sub("^(\r\n|\n)\s*","",title)
                        contenu_ctx[1] = re.sub("\s*(\r\n|\n)\s*"," ",title)
                        #contenu_ctx[1] = self.recup(article,'<b>HD</b>&nbsp;</td><td><b class=["\'][a-z]{2}Headline["\']>','</b>')
                        #contenu_ctx[1] = re.search("\*HD\*\s*\t\*(.*)\*\r\n",article,re.S).group(1)
                        #contenu_ctx[1] = re.search('\<b>HD</b>&nbsp;</td><td><b class="[a-z]{2}Headline">(.*)</b>',article,re.S).group(1)       
                except :
                        contenu_ctx[1] = u'pb de titre'
##                print (contenu_ctx[1])

                s = re.split('<div>',article)
                for t in s:
                        if re.search("\d{1,2}\s{1,}[a-zéèûñíáóúüãçA-Z]*\s{1,}\d{4}</div>",t):
                                date = t[:-6]
                                if re.search("\d{2}:\d{2}</div>", s[s.index(t)+1]):
                                        contenu_ctx[15] = u"REF_HEURE:%s" % t[:-6]
                                        support = s[s.index(t)+2][:-6]
                                else :
                                        support = s[s.index(t)+1][:-6]
                        elif re.search("<td>\d{1,2}\s{1,}[a-zéèûñíáóúüãçA-Z]*\s{1,}\d{4}</td>",t):
                                date = re.search("<td>(\d{1,2}\s{1,}[a-zéèûñíáóúüãçA-Z]*\s{1,}\d{4})</td>",t).group(1)
                                support = self.recup(article,'<b>SN</b>&nbsp;</td><td>','</td>')
##                                support = re.search("\*SN\*\s*\t(.*)\r\n",article).group(1)
                
                #date
                try :
                        #date = re.search("\*PD\*\s*\t(.*)\r\n",article).group(1)
                        #date =  self.recup(article,'<b>PD</b>&nbsp;</td><td>','</td>')
                        date = re.split(" ",date)
                        date[0] = u"%02d" % int(date[0]) #un jour à deux chiffres
                        mois = ["","janvier",u'février',"mars","avril","mai","juin","juillet",u"août", "septembre", "octobre","novembre",u"décembre"]
                        if date[1] not in mois:
                                mois = ["","January",'February',"March","April","May","June","July","August", "September", "October","November","December"]
                        date[1] = u"%02d" % mois.index(date[1])
                        contenu_ctx[5] =   date[0] + "/" + "%s" %date[1] + "/" + date[2][:4]
                except :
                        contenu_ctx[5] = "00/00/0000"
##                print (contenu_ctx[5])
                
                #support
                try :
                        support = re.sub("&amp;","&",support)
                        contenu_ctx[2],contenu_ctx[7],RACINE = self.les_supports.renseigne(support)
                        contenu_ctx[6] = contenu_ctx[2]
                        RACINE = re.sub('\r','',RACINE) #supprimer le \r final
                except :
                        contenu_ctx[2] = u"pb support"
                        contenu_ctx[7] = u"pb support"
                        RACINE = "PBSUPPORT"
##                print (contenu_ctx[2],RACINE)

                #narrateur
                try:
                        contenu_ctx[3] = self.recup(article,'<div class="author">','\s*</div>')
                        #contenu_ctx[3] = re.search  ("\*BY\*\s*\t(.*)\r\n",article).group(1)
                        #contenu_ctx[3] = self.recup(article,'<b>BY</b>&nbsp;</td><td>\s*','\s*</td>')
                except:
                        pass

##                #heure
##                try:
##                        contenu_ctx[15] = u"REF_HEURE:%s" %re.search  ("\*ET\*\s*\t(.*)\r\n",article).group(1)
##                        #contenu_ctx[15] = u"REF_HEURE:%s" % self.recup(article,'<b>ET</b>&nbsp;</td><td>\s*','\s*</td>')
##                except:
##                        pass

##                print (contenu_ctx)

                #récupère les données pour le txt
                contenu_txt = [contenu_ctx[1],'.']  #on commence par le titre

                for paragraphe in re.split('<p class="articleParagraph [a-z]{2}articleParagraph">',article)[1:]:
                        paragraphe = re.split("</p>",paragraphe)[0]
                        paragraphe = re.sub("^(\r\n|\n)\s*","",paragraphe)
                        paragraphe = re.sub("\s*(\r\n|\n)\s*"," ",paragraphe)
                        contenu_txt.extend( [paragraphe] )

                 
                
                
##                if not re.search("nhoc : Headline-Only Content", article):
                        #TXT = self.recup(article,'<p class="articleParagraph [a-z]{2}articleParagraph">','</p>')
                        #TXT = self.recup(article,'<p><b>LP</b>&nbsp;</p></td><td><p class="articleParagraph [a-z]{2}articleParagraph">','</td>')
##                        if re.search ("<p><b>TD</b>&nbsp;</p>",article):
##                                TXT += self.recup(article,'<p><b>TD</b>&nbsp;</p></td><td><p class="articleParagraph [a-z]{2}articleParagraph">','</td>')
##                        TXT = re.sub("(\r\n)|(<p class=\"articleParagraph [a-z]{2}articleParagraph\">)","",TXT)         
##                        TXT = re.sub("</p>","\n",TXT) 
                        #article = re.split("\n\*LP\*\s*\n",article)[1]
                        #article = re.split('<td class="index" align="right" valign="top"><p><b>LP</b>&nbsp;</p></td><td>',article)[1]
                        #article =re.sub("\n\*TD\*\s*\n","",article)
                        #article = re.split("\n\*[A-Z]{2,}\*\s*\n",article)[0]
##                        contenu_txt.append(TXT)



                #écrit les fichiers ctx et txt
                les_fichiers = EcritFichiers(contenu_ctx[5],RACINE,self.rep)
                contenu_ctx = map(ENCODE,contenu_ctx)
                les_fichiers.ecrit(map(enleve_sauts_de_lignes,contenu_ctx),".ctx")
                self.fichiers_generes += 1
                nomTXT = les_fichiers.ecrit(map(ENCODE,contenu_txt),".txt")
                self.fichiers_generes += 1
                return nomTXT
                 

        

if __name__ == "__main__":
        les_supports = "support.publi"
        cpt = 0
        for f in glob.glob("*.htm"):
                prem = parsefactivahtm(f,les_supports)
                print("%s : %d article(s) ; %d inconnu(s)"%(f,prem.Narticles,len(prem.liste_inconnus)))
                for inconnu in prem.liste_inconnus:
                        print ("support inconnu : %s" % (inconnu) )
                prem.traite('.')
                cpt += prem.fichiers_generes
        print ("J'ai écrit %d fichier(s)"%cpt)




