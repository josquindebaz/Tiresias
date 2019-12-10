## -*- coding: utf-8 -*-
#### Nettoyeur caractères
#### version du 31/10/2018
#### Author Josquin Debaz
#### GPL 3

import os, string, re, glob

class liste_TXT(object):
    """liste les textes d'un dossier et de ses sous-dossiers récursivement"""
    def __init__(self,rep):
        self.lesTXT = []
        for roots,dirs,files in os.walk(u'%s'%rep):
            for f in files :
                if ((os.path.splitext(f)[1] == '.txt') or (os.path.splitext(f)[1] == '.TXT')):
                    self.lesTXT.append(os.path.join(roots,f))
                
class agit_dans_un_fichier(object):
    """ouvre, ecrit dans, et ferme un fichier"""
    def __init__(self,fichier):
        self.le_fichier = fichier
        self.buf = open(self.le_fichier,'r').read()
        
    def corrige(self,contenu):
        F = open(self.le_fichier,"w")
        F.write(contenu)
        F.close()
    

class agent_de_surface(object):
    """le nettoyeur de caractères intègre les éléments des scripts de nettoyage de Didier Torny et de Jean-Pierre Charriau"""
    
    def __init__(self,texte):
        self.BUF = texte
        if self.testUTF8(self.BUF):
            self.BUF = self.UTFtoLATIN(self.BUF)
        self.compte_modif = self.les_ascii()
        self.compte_modif += self.les_caracteres()
        self.compte_modif += self.nombres_morceaux()
        self.compte_modif += self.le_tiret()

    def testUTF8(self, txt):
        try:
            txt.decode('UTF-8')
        except UnicodeDecodeError:
            return False
        else:
            return True

    def UTFtoLATIN(self, txt):
        txt = txt.decode('utf-8')
        txt = txt.encode('latin-1', 'xmlcharrefreplace')
        return txt
 
    def les_ascii(self):
        # dictionnaire : [code ascii non reconnu] : [forme reconnue],
        LISTE_DES_CARACTERES = { 156 : "oe" ,   160 : " ", 12 : "\n", 133 : "..." ,
                                 96 : "'" , 145 : "'" , 146 : "'" , 180 : "'" ,
                                 171 :'" ' , 187 : ' "' ,
                                 147 : '"' , 148 : '"' , 186 : '"' ,
                                 149 : "-" , 150 : "-" , 151 : "-" , 173 : "-" , 183 : "-",
                                 }
        n = 0
        for code,nouv_car in LISTE_DES_CARACTERES.iteritems() :
            cherche = string.count(self.BUF,chr(code))
            if cherche :
                self.BUF = string.replace( self.BUF,chr(code), nouv_car)
                
            n += cherche

        return n  

        
    def les_caracteres(self):
        # liste  : balise html à effacer
        Liste_des_balises =['<i>','</i>','<strong>','</strong>','</tr>','<td>','</td>','&lt;i&gt;','&lt;/i&gt;',
                            '&lt;/strong&gt;','&lt;strong&gt;','<em>','</em>','&#65279;',
                            "<div>","</div>","<ul>","</ul>","<p>","<ol>","</ol>","<span>","</span>",
                            "<b>", "</b>", "<p align='center'>", '<p align="CENTER">']
        
        #dictionnaire : "forme corrigée" : ["formes à corriger"],
        carac_multi = {
            "'":["&rsquo;","&#39;",'&#8217;','&#8217;','&#8216;',"&lsquo;"],
            ' " ':["&laquo;","&raquo;","&#8220;","&#8221;","&#171;" ,"&#187;" ,"&quot;","&lt;","&gt;"],
            '... ':["&hellip;","&#8230;","&#x2026;" ]  ,
            u"oe".encode('latin-1'):["&oelig;","&#156;" ,"&#339;", "&#338;" ],
            "-" : ["&#8211;","&#8208;","&sect;","&bull;", "&#8209;"],
            "\n" : ["<br>", "<br/>", "<BR>",  "<BR/>",  "<BR />","<br />",'<tr>',"</p>","</li>","&#8232;"],
            " ":["&nbsp;",'&#xd;','#xd;',"&#160;","&#8201;"],
            u"î".encode('latin-1') :[  "&#238;" ,"&icirc;",u"î".encode('utf-8'), "i&#776;", "i&#770;"],
            u"é".encode('latin-1'):["&eacute;",u"é".encode('utf-8'),"&#233;","e&#769;"],
            u"è".encode('latin-1'):["&egrave;",u"è".encode('utf-8'),"&#232;","e&#768;" ],
            u"à".encode('latin-1'):["&agrave;","&#224;",u"à".encode('utf-8'),"a&#768;"],
            ' - ' : ['&#8212;',"&ndash;"],
            u"â".encode('latin-1'):["a&#770;"],
            u"ô".encode('latin-1'):["&ocirc;","o&#770;","&#244;"],
            u"û".encode('latin-1'):["&ucirc;",  "u&#768;"],
            u"ù".encode('latin-1'):["&ugrave;","&#249;", "u&#768;"],
            u"û".encode('latin-1') : ["u&#770;"],
            u"ê".encode('latin-1'):["&ecirc;","&#234;", "e&#770;"],
            " " : ["&#8203;", "&#8239;"],
            "euros" : ["&#8364;", "&euro;" , "&#8364"], 
            "e": ["&#7497;"],
            u"ç".encode('latin-1'): ["&#231;", "c&#807;", '&ccedil;'],
            u"Ç".encode('latin-1'): ["C&#807;"],
            }
        
        #dictionnaire : "forme corrigée" : "forme à corriger",
        Liste_des_formes= {
#            'é' : 'Ã©' , 'ô' : 'Ã\'' , 'À' : 'Ã¢' , 'û' : 'Ã"' , 'ü' : 'uû' , 'ù' : 'Ã¹' , 'A' : 'Ã€' , 'è' : 'Ã¨' , 'E' : 'Ã‰' , 'E' : 'ÃŠ' , 'ï' : 'Ã¯' ,
#            '-' : 'â€oe' , 'ë' : 'Ã«' , 'ç' : 'Ã§' , 'î' : 'Ã®' , 'ê' : 'Ãª' , 'à' : 'Ã' , "'" : "â€™" ,'oe' : 'Å"', '-' : 'â€"', '-' : 'â€¢', 
             ' " ' : "«" , ' " ' : '»'  , ' ' : "\xc2",
             u"â".encode('latin-1'):"&acirc;",
             u"ï".encode('latin-1'):"&iuml;",
             u"É".encode('latin-1'):"&#201;",
             u"É".encode('latin-1'):"&Eacute;",
             u"â".encode('latin-1') : "&#226;",
             u"ï".encode('latin-1') : "&#239;",
             "&" : "&amp;",
             "&deg;" : "°",
             " ":"&#176;",
             "\n- " : "<li>",
            }
            
        # sépare aussi les marqueurs de parité du type -e-s ou (e) des mots qu'ils connotent
        formes_regexp = { "\\1 -e-s " : "(\S)-e-s" , "\\1 (e) " : "(\S)\(e\)", "\\1 ":"(\S)\r "}
        
        
        n = 0
        for balise in Liste_des_balises:
            cherche = string.count(self.BUF,balise)
            #print balise, cherche
            if cherche:
                #print "A1"
                self.BUF = re.sub( balise,"",self.BUF)
            n += cherche

        #print "A2"


        for correcte,incorrecte in carac_multi.iteritems() :
            for i in incorrecte:
                cherche = string.count(self.BUF,i)
                if cherche:
                    self.BUF = string.replace( self.BUF,i,correcte)
                    n += cherche
                    


        for correcte, incorrecte in Liste_des_formes.iteritems() :
            cherche = string.count(self.BUF, incorrecte)
            if cherche:
                #print "2[%s]%s" %( incorrecte,correcte) 
                self.BUF = string.replace( self.BUF,incorrecte,correcte)
            n += cherche

        for correcte,incorrecte in formes_regexp.iteritems() :
            cherche = len(re.findall(incorrecte,self.BUF))
            if cherche:
                #print "3"
                #print incorrecte, correcte
                self.BUF = re.sub(incorrecte,correcte,self.BUF)
            n += cherche

        return n
    

    def nombres_morceaux(self):
        n = 0
        while len(re.findall("\d \d\d\d|\d\.\d\d\d", self.BUF)):
            n += len(re.findall("\d \d\d\d|\d\.\d\d\d", self.BUF))
            self.BUF = re.sub("(\d)\.(\d\d\d)", "\\1\\2", self.BUF)
            self.BUF = re.sub("(\d) (\d\d\d)", "\\1\\2", self.BUF)
        return n


    def le_tiret(self):
        PONCTUATION=[ ".",",", ";", "!" , "?" , ":" , "'", "(" , ")" , "[" , "]", '\n'] # on définit la liste des signes de ponctuation
        n = 0
        for forme in map(lambda x : "-"+x, PONCTUATION):
            n1 = string.count(self.BUF,forme)
            if n1:
                self.BUF = string.replace(self.BUF,forme," %s %s"%(forme[0],forme[1]))
            n += n1
                
        for forme in map(lambda x : x+"-", PONCTUATION)[1:]:# on ne traite pas la forme .- parce qu'on la trouve dans les abréviations de prénoms composés du type J.-P.
            n2 = string.count(self.BUF,forme)
            if n2:
                self.BUF = string.replace(self.BUF,forme,"%s %s "%(forme[0],forme[1]))
            n += n2
        return n



##class correcteur_ortho(object):
##    def __init__(self,bad):
##        AvAp = "[\s\.,;!?]" #la liste des ponctuations et autres qui peuvent précéder ou suivre une forme à corrige
##        bad =string.join(bad,'|') 
##        motif = "(%s)(%s)(%s)" % (AvAp,bad,AvAp)
##        self.motif_compile = re.compile(motif)
##
##    def agit(self,good,chaine):
##        while (re.search(self.motif_compile,chaine)) :
##            print good
##            chaine = re.sub(self.motif_compile,"\\1%s\\3"%good," %s " %chaine)[1:-1]
##        return chaine




if __name__ == "__main__":
    test = liste_TXT(".")
    n = len(test.lesTXT)
    print ("%d textes" % n)
    if (n):
        cpt = 0
        for f in test.lesTXT:
            F = agit_dans_un_fichier(f)
            N = agent_de_surface(F.buf)
            F.corrige(N.BUF)
        cpt +=  N.compte_modif
        print ("%d modifications" % cpt)

