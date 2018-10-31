# -*- encoding: iso-8859-1 -*-
#----------------------------------------------------------
#Script de traitement de xml issus de LEXIS NEXIS pour Prospéro
#Génère les TXT et les CTX à partir des fichiers txt du dossier
#version du 31/10/2018 
#Josquin Debaz
#GNU General Public License
#Version 3, 29 June 2007
#See http://www.gnu.org/licenses/ or COPYING.txt for more information.
#----------------------------------------------------------

import glob,os,re,codecs

def enleve_sauts_de_lignes(data):
        data = re.sub('\s',' ',data)
        try :
                return data.encode('latin1')
        except :
                return data

def ENCODE(UNICODE):
        #Des gremlins utf-8
        #http://www.eki.ee/letter/
        table = [
                ['<b>',''],
                ['</b>',''],
                ['«','"'],
                ['»','"'],
                ['&nbsp;',' '],
                ['&gt;','>'],
                ['&amp;','&'],
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
                ]

        for T in table:
                UNICODE = re.sub(T[0],T[1],UNICODE)

        try:
                LATIN = UNICODE.encode('latin_1','strict')
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
                        #print support
                        this_support = re.split('; ',support[:-1])
                        self.supports.append(this_support) 
                        self.supports_clefs.append(this_support[0])
                
        def renseigne(self,source):
                try:
                        #print source
                        clef = self.supports_clefs.index(source)
                except ValueError:
                        LOGS = open('log_inconnus.txt','a').write((source.encode('latin_1','xmlcharrefreplace') + "\n"))
                        #print("Un support inconnu : %s" % source)
                        return (['INCONNU'] * 3)
                else :
                        #print(self.supports[clef][1:])
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
                while os.path.isfile(os.path.join("LN",nom + ".txt")): #tant que le fichier existe
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



class parseLEXISNEXIS(object):
        def __init__(self, fichier, cheminSupports, dest):
            self.les_supports = supports(cheminSupports)
            self.dest = dest
            self.listeFichiersecrits = []
            self.supportsInconnus = []
            b = codecs.open(fichier, 'r', encoding='utf-8', errors='strict').read()

            try:
                L = re.split('Dokument \d* von \d*', b)[1:]
                lang = 'ALL'
            except:
                L = re.split('Document \d* de \d*',b)[1:]
                L[-1] = re.split("\r\n---- FIN ----",L[-1])[0]
                
            n = len(L)
            print ("Il y a %s article(s) dans ce fichier"  % n)
            while(L):
                article = L.pop(0)
                #print ("Il reste %d articles à traiter" % (len(L)))
                if (lang == "ALL"):
                    self.traite_articleALL(article)
                else:
                    self.traite_article(article)

        def traite_articleALL(self, article):
            """Function for german articles"""

            if re.search("\r\nLÄNGE: \d* \S*\r\n", article):
                en_tete, article = re.split('\r\nLÄNGE: \d* \S*\r\n', article, 1)
            elif(re.search("\r\nLENGTH: \d* \S*\r\n", article)):
                en_tete, article = re.split('\r\nLENGTH: \d* \S*\r\n', article, 1)
            if re.search("\r\nUPDATE:.*\r\n", article):                
                article, pied = re.split("UPDATE:", article)
            elif re.search("\r\nLOAD-DATE:.*\r\n", article):                
                article, pied = re.split("LOAD-DATE:", article)


            #récupère les données pour le ctx
            contenu_ctx = ["fileCtx0005", "titre", "auteur", "", "", "date", "support", "type support",  "", "",  "", "", "", "n", "n", ""]
            support = re.search("^\s*(.*)\r\s*", en_tete).group(1)
            support = self.les_supports.renseigne(support)
            RACINE = re.sub('\r',"",support[2])
            if (support[0] != 'INCONNU'):
                contenu_ctx[2] = support[0]
                contenu_ctx[6] =  contenu_ctx[2]   #le journal
                contenu_ctx[7] = support[1]                     #type support
            else :
                self.supportsInconnus.append(en_tete[1])
                contenu_ctx[2] = contenu_ctx[6] = en_tete[1]
                contenu_ctx[7] = "type support inconnu"

            if re.search("AUTOR: ", en_tete):
                #recupere narrateur
                contenu_ctx[3] = u"%s"%re.search("AUTOR: (.*)\r", en_tete).group(1)

            #gere la date    
            date = re.search("(\d{1,2}\. \S* \d{4})", en_tete).group(1)
            date = re.split(" ", date)
            mois = {u"janvier":"01", u'février':"02", "mars":"03", "avril":"04", 
                "mai":"05",  "juin":"06",  "juillet":"07", u"août":"08",  
                "septembre":"09",  "octobre":"10", "novembre":"11", u"décembre":"10", 
                 u"Janvier":"01", u'Février':"02", "Mars":"03", "Avril":"04", "Mai":"05", 
                 "Juin":"06", "Juillet":"07",u"Août":"08", "Septembre":"09", 
                 "Octobre":"10","Novembre":"11",u'D\xe9cembre':"12", 
                 "Januar": "01", u'Februar' : "02", u'M\xe4rz' : "03", 
                 u'April' : "04", u'Mai' : "05", u'Juni' : "06",  u'Juli' : "07", 
                 u'August' :  "08",  u'September' : "09", u'Oktober' : "10", 
                 u'November' : "11", u'Dezember' : "12"}
            if date[1] not in mois:
                    print ("this month is not in my list ", date)
            else :
                    date[1] = mois[date[1]]

            date[0] = u"%02d"    % int(date[0][:-1])
            contenu_ctx[5] =   date[0] + "/" + "%s" %date[1] + "/" + date[2][:4]

            #recupere titre
            tit1 = re.split("\d{4}\r\n\r\n", en_tete, 1)[1]
            contenu_ctx[1] = re.sub("\r\n", " ", re.split("\r\n\r\n[A-Z]*\:", tit1, 1)[0])
            #contenu_ctx[1] = re.split("\n", en_tete)[8]
            #change this character
            contenu_ctx[1] = re.sub(u'\u201e', '"', contenu_ctx[1])

            contenu_txt = re.sub("HIGHLIGHT:\s*", "", article)
            contenu_txt = [contenu_ctx[1] , "." , contenu_txt]


            #écrit les fichiers ctx et txt
            les_fichiers = EcritFichiers(contenu_ctx[5], RACINE, self.dest)
            
            contenu_ctx = map(enleve_sauts_de_lignes, contenu_ctx)
            try:
                self.listeFichiersecrits.append(les_fichiers.ecrit(contenu_ctx, ".ctx"))
            except:
                print contenu_ctx
            self.listeFichiersecrits.append(les_fichiers.ecrit(map(ENCODE, contenu_txt), ".txt"))



        def traite_article(self,article):
            article = re.split('\r\nDATE-CHARGEMENT:',article)[0]
            if re.search("ORIGINE-DEPECHE:",article):
                    en_tete,article = re.split('\r\nORIGINE-DEPECHE: .*\r\n',article,1)
            elif re.search("\r\nLONGUEUR: \d* \S*\r\n",article):
                    en_tete,article = re.split('\r\nLONGUEUR: \d* \S*\r\n',article,1)
            elif re.search('\r\nRUBRIQUE: .*\r\n',article):
                    en_tete,article = re.split('\r\nRUBRIQUE: .*\r\n',article,1)
            
            #récupère les données pour le ctx
            contenu_ctx = ["fileCtx0005","titre","auteur","","","date","support","type support", "","", "","","","n","n",""]
            en_tete = re.sub('(\r\n){1,}\s*',"\t",en_tete)
            en_tete = re.split("\t",en_tete)

            #gère le support
            support = self.les_supports.renseigne(en_tete[1])
            RACINE = re.sub('\r',"",support[2])
            if (support[0] != 'INCONNU'):
                contenu_ctx[2] = support[0]
                contenu_ctx[6] =  contenu_ctx[2]   #le journal
                contenu_ctx[7] = support[1]                     #type support
            else :
                self.supportsInconnus.append(en_tete[1])
                contenu_ctx[2] = contenu_ctx[6] = en_tete[1]
                contenu_ctx[7] = "type support inconnu"

            #gere la date    
            date = re.search("(\d{1,2} \S* \d{4})",en_tete[2]).group(1)
            date = re.split(" ",date)
            mois = {u"janvier":"01",u'février':"02","mars":"03","avril":"04","mai":"05","juin":"06",
                    "juillet":"07",u"août":"08", "septembre":"09", "octobre":"10","novembre":"11",u"décembre":"10",
                    u"Janvier":"01",u'Février':"02","Mars":"03","Avril":"04","Mai":"05","Juin":"06",
                    "Juillet":"07",u"Août":"08", "Septembre":"09", "Octobre":"10","Novembre":"11",u'D\xe9cembre':"12",}
            if date[1] not in mois:
                    print (date)
            else :
                    date[1] = mois[date[1]]

            date[0] = u"%02d"    % int(date[0])

            contenu_ctx[5] =   date[0] + "/" + "%s" %date[1] + "/" + date[2][:4]

            #gere le titre
            sous_titre = 0
            try :                           
                    contenu_ctx[1] = en_tete[3]
            except :
                    print (en_tete)
                    contenu_ctx[1] = "sans titre"

            if re.search("AUTEUR:", en_tete[4]):
                    contenu_ctx[3] = re.search("AUTEUR: (.*)",en_tete[4]).group(1)
            elif not ( re.search("^[A-Z]{2,}:", en_tete[4])):
                    sous_titre = en_tete[4]

            
            #récupère les données pour le txt
            contenu_txt = [contenu_ctx[1],'.']  #on commence par le titre
            if (sous_titre):
                    contenu_txt.append(sous_titre)
            article = re.sub(u"\r\nENCART:.*\r\n","",article)
            contenu_txt.append(article)

            #écrit les fichiers ctx et txt
            les_fichiers = EcritFichiers(contenu_ctx[5],RACINE,self.dest)
            
            #print (contenu_ctx)
            contenu_ctx = map(enleve_sauts_de_lignes,contenu_ctx)
            self.listeFichiersecrits.append(les_fichiers.ecrit(contenu_ctx,".ctx"))
            self.listeFichiersecrits.append(les_fichiers.ecrit(map(ENCODE,contenu_txt),".txt"))
            
            

    


if __name__ == '__main__' :
    if not  os.path.isfile("support.publi") :
        print("Il me manque le support.publi")
    else :
        les_supports = supports("support.publi")
    liste_fichiers_txt = glob.glob('*.txt')
    if 'COPYING.txt' in liste_fichiers_txt :
            liste_fichiers_txt.remove('COPYING.txt')
    if 'log_inconnus.txt' in liste_fichiers_txt :
            liste_fichiers_txt.remove('log_inconnus.txt')
    if 'log_gremlins.txt' in liste_fichiers_txt :
            liste_fichiers_txt.remove('log_gremlins.txt')
    n = len(liste_fichiers_txt)
    while liste_fichiers_txt:
        fichier = liste_fichiers_txt.pop(0)
        print("Je traite %s,  il reste %d fichiers" % (fichier, len(liste_fichiers_txt)))
        parseLEXISNEXIS(fichier, 'support.publi', 'result')
