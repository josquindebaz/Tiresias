# -*- encoding: iso-8859-1 -*-
#----------------------------------------------------------
#Script de Script de récupération des Questions parlementaires pour Prospéro
#version du 23/10/2018
#Josquin Debaz
#GNU General Public License
#Version 3, 29 June 2007
#See http://www.gnu.org/licenses/ or COPYING.txt for more information.
#----------------------------------------------------------

verbose = 0


##from Tkinter import *
import re, urllib, urllib2, os #, glob, tkFileDialog, string, time,


#---------------------------------
#Les listes

groupes = {#groupes du Sénat
    "CRC" : u"Groupe Communiste Républicain et Citoyen",
    "SOC" : u"Groupe Socialiste",
    "UC" : u"Groupe Union centriste - UDF",
    "UC-UDF" : u"Groupe Union centriste - UDF",
    "RDSE" : u"Groupe du Rassemblement Démocratique et Social Européen",
    "UMP" : u"Groupe Union pour un Mouvement Populaire",
    "NI" : u"Réunion administrative des Sénateurs ne figurant sur la liste d'aucun groupe",
    "RI"  : u"Groupe des Républicains Indépendants",
    "RPR": u"Groupe du Rassemblement pour la République",
    "CRARS" : u"Centre Républicain d'Action Rurale et Sociale",
    "COM" : u"Groupe Communiste",
    "GD" : u"Groupe de la Gauche Démocratique",
    "RDE" : u"Groupe du Rassemblement Démocratique Européen",
    "RIAS" : u"Groupe des Républicains Indépendants d'Action Sociale",
    "UCDP" : u"Groupe de l'Union Centriste des Démocrates de Progrès",
}

natures = {
    'QE' : u'Question écrite',
    'QG' : u'Question au Gouvernement',
    'QOSD' : u'Question orale sans débat',
}


#fin des listes
#---------------------------------



class fouilleASS(object):
    "Fait une recherche sur le site de l'Assemblée"

    def __init__(self,texte,leg):

        self.listeASS = []
        self.listeLiens = []
        self.nbre_questions = 0
        
        for L in self.telec(texte,leg):
            self.listeASS.extend(self.recupereQuestions(L))

    def reqAss(self,leg,recherche,limit):
        url = "http://www2.assemblee-nationale.fr/recherche/resultats_questions/index.asp?legislature"

        headers = {
            'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
            'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded'
        }


        #convert keyword to utf-8
        recherche = recherche.decode('latin-1').encode('utf-8')

        
        formData = (
            ('legislature', leg),
            ('q',recherche),
            ('q_in',0),
            ("limit",limit),
            )

       
        encodedFields = urllib.urlencode(formData)


        req = urllib2.Request(url, encodedFields, headers)

        return urllib2.urlopen(req).read()


            
    def telec(self,texte,leg):
        resultat = []
        #NumLegislature de 7Questions à 13Questions
        for L in leg :
##            url = "http://recherche2.assemblee-nationale.fr/questions/resultats-questions.jsp?ResultCount=200&ResultStart=1&SortField=DPQ_NUM&SortOrder=Croissant&T2=%s&NumLegislature=%sQuestions" % (re.sub(' ',',',texte),int(L)+7)
##            result = urllib.urlopen(url).read()
##            if (not re.search('Aucun r&eacute;sultat trouv&eacute; pour cette recherche',result)):
##                if (re.search(">(\d*)</span> questions",result)):
##                    nb_q = int(re.search(">(\d*)</span> questions",result).group(1))
##                    self.nbre_questions += nb_q
##                    if (nb_q > 200):
##                        url = "http://recherche2.assemblee-nationale.fr/questions/resultats-questions.jsp?ResultCount=%d&ResultStart=1&SortField=DPQ_NUM&SortOrder=Croissant&T2=%s&NumLegislature=%sQuestions" % (nb_q,re.sub(' ',',',texte),int(L)+7)
##                        result = urllib.urlopen(url).read()
##                    resultat.append(result)
##                else :
##                    print "l79 result"
            L = int(L)+7
            teste_nb_questions = self.reqAss(L,texte,10)
            if (not re.search('<p>Aucun r..sultat trouv.. pour cette recherche.</p>',teste_nb_questions)):
                if re.search("<p><strong>(\d*)</strong> questions trouv..es pour votre recherche</p>",teste_nb_questions):
                    nb_q = int(re.search("<p><strong>(\d*)</strong> questions trouv..es pour votre recherche</p>",teste_nb_questions).group(1))
                    result = self.reqAss(L,texte,nb_q)  
                    resultat.append(result)
                else :
                    print "pb nb questions assemblee : leg %d, recherche [%s]" %(L,s)
            else :
                print "legislation %d : aucune question assemblee trouvee" %(L)
        
        return resultat
        
    def recupereQuestions(self,buf):
        listeQP =[]
##        for Q in re.split('<form target="Question"',buf)[1:]:
##            lien = re.search('http://questions.assemblee-nationale.fr/.*.htm',Q).group(0)
##            num = re.search('<b>.*ème législature - (.*)</b>',Q).group(1)
##            date = re.search('Publi&eacute;e au JO le <b>(.*)</b>',Q).group(1)
##            auteur = re.search('<div style="font-size:12px;"><b>(.*)</b>',Q).group(1)
##            theme = re.search('<i>(.*)</i>',Q).group(1)
##            if (re.search("R&eacute;ponse JO",Q)) :
##                reponse = " : R"
##            else :
##                reponse = ""
##            question = "%s : %s%s : %s : %s " % (date,num,reponse,auteur,theme)
##            listeQP.append(question)
##            self.listeLiens.append(lien)
##        #listeQP.reverse()
        for Q in re.split('<tr>',buf)[2:]:
##            print Q
            lien = re.search('http://questions.assemblee-nationale.fr/.*.htm',Q).group(0)
##            print lien
            num = re.search('<strong>.*me l.*gislature - (.*)</strong>',Q).group(1)
##            print num
            date = re.search('Publi..e au JO le\s*<strong>(.*)</strong>',Q).group(1)
##            print date
            auteur = re.search('<td class="text-center">\s*<strong>(.*)</strong>',Q).group(1)
##            print auteur
            theme = re.search('<em>(.*)</em>',Q).group(1)
##            print theme
            if (re.search("R..ponse JO le",Q)) :
                reponse = " : R"
            else :
                reponse = ""
##            print reponse
            question = "%s : %s%s : %s : %s " % (date,num,reponse,auteur,theme)
##            print question
            listeQP.append(question)
            self.listeLiens.append(lien)
##        listeQP.reverse()
        return listeQP     


class fouilleSENAT(object):
    "Fait une recherche sur le site du Sénat"

    def __init__(self,mots_clefs,de,au):
        self.listeSENAT = []
        self.listeLiens = []
        
        html = self.telecpageweb(mots_clefs,de,au)
        if (not re.search("Il n'y a aucun résultat pour cette recherche.",html)):
            try:
                self.nbre_questions = re.search("(\d*)\r\n *\r\n *question",html).group(1)
		##print self.nbre_questions
            except:
                self.nbre_questions = re.search("(\d*)\r\n *question",html).group(1)
            self.listeSENAT = self.recupereQuestions(html)
            if (self.nbre_questions > 10):                
                for cpt in range(10,int(self.nbre_questions),10):
                    self.listeSENAT.extend(self.recupereQuestions(self.telecpageweb(mots_clefs,de,au,cpt)))
        else :
            self.nbre_questions = 0
	

    def telecpageweb(self,mots_clefs,de,au,off=0):
    #aff=ens afficher ensemble avec et sans réponse (sep sinon)
    #off = 0 = page 1 ; 10 = page 2
    #rch=qs question simple
    #de date départ yyyymmjj
    #au date arrivée yyyymmjj
    #radio=deau
    #tri : p pertinence, dd date descendante, da date ascendante
    #_c=MC1+MC2

        #vérifier que la date de départ soit > 78
        if (int(re.split("/",de)[2]) < 1978):
            de = "01/01/1978"
            
        tri = "da"
        url = "http://www.senat.fr/basile/rechercheQuestion.do?aff=ens&off=%d&rch=qs&de=%s&au=%s&radio=deau&tri=%s&_c=%s" % (off,de,au,tri,re.sub(' ','+',mots_clefs))
##        print (url)
##        buf = urllib.urlopen(url).read()
##        print (buf)
##        return buf
        return  urllib.urlopen(url).read()

    def recupereQuestions(self,buf):
        listeQP = []
        #buf = re.split("OnMouseOver",buf)
        #print re.findall('.*document-03.*',buf)
        #buf = re.split('<div class="document document-03">',buf)
        buf = re.split('<div class="document document-\d*"',buf)
##        print [len(buf)]
        for q in buf[1:]:

            lien = re.search("visio.do\?id=(.*)&amp;idtable=",q).group(1)
            date = re.search("\d\d/\d\d/\d\d\d\d",q).group(0)
            num = re.search('Question n&deg; (\S*)',q).group(1)
            
            nom = re.search('posée par\s*(\S*\s*\S*\s*\S*)',q).group(1)
            nom = re.sub("(\r\n)", " ",nom)
            nom = re.sub("                        "," ",nom)

            try:
                titre = re.search("<b>(.*)</b>",q).group(1)
            except:
                try:
                    titre = re.search("<b>(.*)\s*</b>",q).group(1)
                except :
                    titre =  re.search(">\r\n\s*(.*)\r*\n*\r\s*</a>",q).group(1)

            titre = re.sub("&#39;","'",titre)
            titre = re.sub("&quot;",'"',titre)

            if (re.search("En attente de réponse",q)):
                reponse = ""
            else:
                reponse = " : R"
            
            question = "%s : %s%s : %s : %s" % (date,num,reponse,nom,titre)
            question = question.decode('latin1')
            listeQP.append(question)
            self.listeLiens.append(lien)

        return listeQP


class parseSENAT(object):

    def __init__(self,buf):            

        buf = buf.decode('latin1')

        if (verbose): print "je me lance 1"

        texte = re.split('haut"></a>',buf) 
        texte = re.split('<!-- Affichage',texte[1])
        
        if (verbose): print "je commence a reperer des donnees"

        self.donnees = {}

        if (verbose): print "legislation"
        try :
            self.donnees['leg'] = re.search('(\d*)\s*<sup>&egrave;me</sup> l&eacute;gislature',texte[0]).group(1)
        except :
            self.donnees['leg'] = re.search('(\d*)\s*<sup>e</sup> l&eacute;gislature',texte[0]).group(1)
        
        if (verbose): print "num"
        self.donnees['num'] = re.search('n&deg;\s*(.*)\r',texte[0]).group(1)

        if (verbose): print "auteur"
        self.donnees['aut'] = re.search('de\s*<b>\s*.*\s*.* M.*\s*(.*)',texte[0]).group(1)
##        self.donnees['aut'] = re.sub("\s{1,}"," ",self.donnees['aut'])

	
        try :
            prec = re.search('<span class="rouge">\s*(.*)',texte[0]).group(1)
        except :
            prec =  re.search("</b>\s*\((.*)\)",texte[0]).group(1)

        if (verbose): print "groupe"
        prec = re.split(' - ',prec)
        groupe = prec[1]            

        try: groupes[groupe]
        except :
            self.donnees['groupe'] = groupe
        else:
            self.donnees['groupe'] = groupes[groupe]
	
        if (verbose): print "departement"
        self.donnees['dept'] = prec[0]
        nat = re.search('\s*(.*)\s*n&deg;',texte[0]).group(1)

        if (verbose): print "nature"
        self.donnees['nature'] = re.sub('&#39;', "'",nat)
	
        if (verbose): print "publication"
        try :
            self.donnees['dpq'] = re.search('<span class="rouge">publi&eacute;e.*\s*([\d/]*)',texte[0]).group(1)
        except :
            self.donnees['dpq'] = re.search('publi&eacute;e dans le JO S&eacute;nat du\s*([\d/]*)',texte[0]).group(1)
        try:
            self.donnees['pgq'] = re.search('- page\s*(\d*)',texte[0]).group(1)
        except:
            print "pb pagination question"
            self.donnees['pgq'] = ""

        #avec ou sans réponse ?
        if re.search('Réponse',texte[0]):
            if (verbose): print "avec reponse"
            self.donnees['ASREP'] = "Avec réponse"
            self.donnees['ministere'] = re.search('Réponse du (.*)',texte[0]).group(1)
            texte = re.split('<p align="justify">',texte[0])
            try :
                self.donnees['dpr'] = re.search('publi&eacute;e dans le JO S&eacute;nat du\s*(.*)\s',texte[2]).group(1)
                self.donnees['pgrep'] = re.search('- page\s*(\d*)',texte[2]).group(1)
            except:
                try:
                    self.donnees['dpr'] = re.search('publi&eacute;e dans le JO S&eacute;nat du\s*(.*)\s',texte[3]).group(1)
                except:
                    self.donnees['dpr'] = re.search('publi&eacute;e dans le JO S&eacute;nat du\s*(.*)\s',texte[2]).group(1)
                try :
                    self.donnees['pgrep'] = re.search('- page\s*(\d*)',texte[3]).group(1)
                except:
                    self.donnees['pgrep'] = ""
            self.donnees['dpr'] = re.sub('\s', '', self.donnees['dpr'])

        else:
            if (verbose): print "sans reponse"
            
            
            self.donnees['ASREP'] = "Sans réponse"
            if (not re.search('réponse du',texte[0])):
                if (verbose):
                    print "pb ministere"
                rapport = u"problème ministère %s : %s\n" % (self.donnees['leg'],self.donnees['num'])
                self.donnees['ministere'] = ""
                #listbox.insert(0,rapport)
            else:
                if re.search("\S*La question est caduque", texte[0]):
                    if (verbose): print "La question est caduque"
                    self.donnees['ministere'] =  re.search("\S*Transmise au (.*)\r", texte[0]).group(1)
                else:
                    if (verbose): print "en attente"
                    self.donnees['ministere'] = re.search('En attente de réponse du\s*(.*)',texte[0]).group(1)
            texte = re.split('<p class="justifie">',texte[0])
            if (len(texte) < 2) : texte = re.split('<p align="justify">',texte[0])

        if (verbose): print "je recupere la question"            
         
        question = re.split('</p>',texte[1])[0]
        self.donnees['question'] = re.sub('<br/>\s*','\n',question)
        

        if (self.donnees['ASREP'] == "Avec réponse"):
            if (verbose): print "je traite la reponse"
            if not( re.search('<br/>\s*',texte[3])):
                if (verbose): print "REP1",
                if re.search("<h2>\s*R.ponse du Ministère.*", texte[3]):
                    if (verbose): print "2"
                    reponse = re.split('</p>\r\n',texte[4])[0]
                else:
                    if (verbose): print "1"
                    reponse = re.split('</p>\r\n',texte[3])[0]
                reponse = re.sub("(</p><p>|<p>)","\n",reponse)
                self.donnees['reponse'] = reponse
            else :
                if (verbose): print "REP2"
                try:
                    reponse = re.split('<p>',texte[3])
                    reponse = re.split('</p>',reponse[0])
                    reponse = re.sub('Réponse. - ','',reponse[0])
                    self.donnees['reponse'] = re.sub('<br/>\s*','\n',reponse)
                except:
                    if (verbose): print "REP3"
                    reponse = re.split('Réponse',texte[1])
                    self.donnees['reponse'] = re.sub('<br/>\s*','\n',reponse[1])

        if (verbose): print "j'ai fini"
                

class parseASS2(object):
    def __init__(self,buf):
##        buf = buf.decode('utf-8').encode("cp1252")
        buf = buf.decode('utf-8')
        self.donnees = {}
        self.donnees['leg']=re.search('<td class="tdstyleh1">(\d*)',buf).group(1)
        self.donnees['num']=re.search(u"Question N° : <b>(.*)</b>",buf).group(1)
        depute = re.search('<td class="tdstyleh3">de(.*)',buf).group(1)
        self.donnees['aut'], self.donnees['groupe'], self.donnees['dept'] = re.search("<b>(.*)</b> \(.(.*) - (.*).\)",depute).group(1,2,3)
        self.donnees['aut'] = re.sub("M\..|Mme.","",self.donnees['aut'])
        self.donnees['ministere'] = re.search('Minist.*re attributaire &gt; <span class="contenu">(.*)</span>',buf).group(1)
        self.donnees['nature'] = re.search('<td class="tdstyleh3">\s*<b>(.*)</b>',buf).group(1)
        if ((self.donnees['nature'] == u"Question écrite") or (self.donnees['nature'] == u"Question orale sans débat")):
            if (verbose): print "nature 1"
            if re.search("Réponse publiée",buf):
                self.donnees['ASREP'] = "Avec réponse"
                JO = re.split(u"Réponse",re.search('Question publi.*',buf).group(0))
                self.donnees['dpq'], self.donnees['pgq'] =  re.search("<b>(.*)</b>.page :.<b>(\d*)</b>",JO[0]).group(1,2)
                self.donnees['dpr'], self.donnees['pgrep'] = re.search("<b>(.*)</b>.page :.<b>(\d*)</b>",JO[1]).group(1,2)
                textes = re.split('<h2> Texte de la question</h2>\s*.*<div class="contenutexte">',buf)[1]
                self.donnees['question']= re.split("</div>",textes)[0]
                reponse = re.split("</div>",textes)[1]
                self.donnees['reponse'] = re.split('<div class="contenutexte">',reponse)[1]
                if (self.donnees['nature'] == u"Question orale sans débat"):
                    self.donnees['reponse'] = self.prepare_reponse(self.donnees['reponse'])
            else :
                self.donnees['ASREP'] = "Sans réponse"
                JO = re.search('Question publi.*',buf).group(0)
                try :
                    self.donnees['dpq'], self.donnees['pgq'] =  re.search("<b>(.*)</b>.page :.<b>(\d*)</b>",JO).group(1,2)
                except :
                    self.donnees['dpq'] = re.search("<b>(.*)</b>",JO).group(1)
                    self.donnees['pgq'] = ""
                    
                self.donnees['question'] = re.split("</div>",re.split('<div class="contenutexte">',buf)[1])[0]
        elif (self.donnees['nature'] == "Question au Gouvernement"):
            if (verbose):
                print "nature 2"            
            self.donnees['ASREP'] = "Sans réponse"
            self.donnees['dpq'], self.donnees['pgq'] =  re.search('Réponse publi.*<b>(.*)</b>.*<b>(\d*)</b>',buf).group(1,2)
            question = re.split("</div>",re.split('<div class="contenutexte">',buf)[1])[0]
            self.donnees['question'] = self.prepare_reponse(question)

    def prepare_reponse(self,texte):
        texte = re.sub("<p align='center'>(.*)</p>","\\1\n.\n",texte)
        texte = re.sub("<br/>|<br />","\n",texte)
        texte = re.sub("<b>(.*).</b>","(LOC \\1)",texte)
        texte = re.sub("<i>|</i>|<em>|</em>","",texte)
        return texte
        
class parseASS3(object):
    def __init__(self, buf):
        buf = buf.decode('utf-8')
        self.donnees = {}
        #legislation
        self.donnees['leg']=re.search('<header class="question_legislature">(\d*)', buf).group(1)
        #no question
        self.donnees['num']=re.search(u'id="question_col10"> Question N° (.*)</div>', buf).group(1)
        #depute and group and department
        depute = re.search('title="Lien vers la fiche de.* target="_blank">(.*)</div>', buf).group(1)
        aut, self.donnees['groupe'], self.donnees['dept'] = re.search("(.*)</a></span> \((.*) - <span>(.*)</span>", depute).group(1, 2, 3) 
        self.donnees['aut'] = re.sub("M\..|Mme.", "", aut)
        #minister
        self.donnees['ministere'] = re.search('Minist.re attributaire > </span> (.*)', buf).group(1)

        #type of question
        if re.search('id="question_col10">Question .crite</div>', buf):
            self.donnees['nature'] = u"Question écrite"
        elif re.search('id="question_col10">Question au gouvernement</div>', buf):
            self.donnees['nature'] = "Question au Gouvernement"
        elif re.search('id="question_col10">Question orale sans d.bat</div>', buf):
            self.donnees['nature'] = u"Question orale sans débat"

        #type QE and QOSD
        if ((self.donnees['nature'] == u"Question écrite") or (self.donnees['nature'] == u"Question orale sans débat")):

            if (verbose): print "nature QE/QOSD"
            
            #dates and pages
            JO1 = re.search("<div>Question publi.*", buf).group(0)
            self.donnees['dpq'] = re.search(">(\d*/\d*/\d*)</span>", JO1).group(1)
            try:
                self.donnees['pgq'] = re.search(".*page.*>(\d*)</a></span></div>", JO1).group(1)
            except:
                self.donnees['pgq'] = u"s.p."

            #response
            if re.search("Réponse publiée",buf):
                if verbose: print "avec reponse"
                self.donnees['ASREP'] = "Avec réponse"
                
                #dates and pages
                JO2 = re.search("<div>R.ponse publi.*", buf).group(0)
                self.donnees['dpr'] = re.search(">(\d*/\d*/\d*)</span>", JO2).group(1)
                try:
                    self.donnees['pgr'] = re.search(".*page.*>(\d*)</a></span></div>", JO2).group(1)
                except:
                    self.donnees['pgr'] = re.search(".*page.*>(\d*)</span></div>", JO2).group(1)

                #response content
                Rcontent = re.split('<div class="reponse_contenu">', buf)[1]
                Rcontent = re.split('</div>', Rcontent)[0]
                self.donnees['reponse'] = Rcontent

                if (self.donnees['nature'] == u"Question orale sans débat"):
                    self.donnees['reponse'] = self.prepare_reponse(self.donnees['reponse'])

            else:
                self.donnees['ASREP'] = "Sans réponse"

            #question content
            Qcontent = re.split('<h3>Texte de la question</h3>', buf)[1]
            Qcontent = re.split('</div>', Qcontent)[0]
            Qcontent = re.sub("(<p>|</p>)", "", Qcontent)
            self.donnees['question'] = Qcontent


                
        #QG
        elif (self.donnees['nature'] == "Question au Gouvernement"):
            if (verbose): print "nature QG"            
            self.donnees['ASREP'] = "Sans réponse"
            #dates and pages
            JO2 = re.search("<div>R.ponse publi.*", buf).group(0)
            #print JO2
            self.donnees['dpq'] = re.search(">(\d*/\d*/\d*)</span>", JO2).group(1)
            self.donnees['pgq'] = re.search(".*page.*>(\d*)</span></div>", JO2).group(1)
            question = re.split('<div class="reponse_contenu">', buf)[1]
            question = re.split('</div>', question)[0]
            self.donnees['question'] = self.prepare_reponse(question)

        if verbose : print self.donnees

    def prepare_reponse(self, texte):
        texte = re.sub('\s*</p><p align="CENTER"> (.*) <a.*</a> </p>', "\\1\n.\n", texte)
        texte = re.sub("<br/>|<br />|<br>", "\n", texte)
        texte = re.sub("<strong>(.*).*</strong>", "\n(LOC \\1) ", texte)
        texte = re.sub("<i>|</i>|<em>|</em>|<p>|</p>", "", texte)
        return texte
 

class parseASS(object):

    def __init__(self,buf):
        self.donnees = {}
        self.donnees['leg']=re.search('<LEG>(\d.*)ème législature</LEG>',buf).group(1)
        self.donnees['num']=re.search('<NUM>(.*)</NUM>',buf).group(1)
        self.donnees['aut']=re.search('<AUT>(.*) (.*)</AUT>',buf).group(1)
        self.donnees['groupe']=re.search('<GROUPE>(.*)</GROUPE>',buf).group(1)
        nat=re.search('<NAT>(.*)</NAT>',buf).group(1)
        self.donnees['nature'] = natures[nat]
        self.donnees['dept']=re.search('<DEPT>(.*)</DEPT>',buf).group(1)
        self.donnees['dpq']=re.search('<DPQ>(.*)</DPQ>',buf).group(1)
        self.donnees['pgq']=re.search('<PGQ>(.*)</PGQ>',buf).group(1)
        self.donnees['ministere'] = re.search('<MINA>(.*)</MINA>',buf).group(1)
            
        if (nat == "QE") :
            try :
                re.search('<REP>(.*)</REP>',buf).group(1)
                if (re.search('<REP>(.*)</REP>',buf).group(1) == "") :
                    self.donnees['ASREP'] = "Sans réponse"
                else :
                    self.donnees['ASREP'] = "Avec réponse"
                    self.donnees['dpr']=re.search('<DPR>(.*)</DPR>',buf).group(1)
                    self.donnees['pgrep']=re.search('<PGREP>(.*)</PGREP>',buf).group(1)
            except:
                self.donnees['ASREP'] = "Avec réponse"
                self.donnees['dpr']=re.search('<DPR>(.*)</DPR>',buf).group(1)
                self.donnees['pgrep']=re.search('<PGREP>(.*)</PGREP>',buf).group(1)
                
        if (nat == "QOSD") :
            self.donnees['ASREP'] = "Avec réponse"
            self.donnees['dpr']=re.search('<DPR>(.*)</DPR>',buf).group(1)
            self.donnees['pgrep']=re.search('<PGREP>(.*)</PGREP>',buf).group(1)
        
        if (nat == "QG") : #Les questions au gouvernement
            #récupère la page
            self.donnees['pgq'] =  re.search('<PGREP>(.*)</PGREP>',buf).group(1)
            #sépare le texte
            if re.search("<REPONSE>", buf):
                texte = [re.split('DEBAT : ', buf)[1]]
            else:
                texte= re.split('<REP>',buf)
                texte = re.split('</REP>',texte[1])
                
            #Le titre
            texte = re.sub('(</a></p>)|(</A></P>)','\n.\n', texte[0])
            #Les locuteurs -----------------------
            texte = re.sub(' *<(strong|STRONG)> *',r'(LOC ',texte)
            texte = re.sub('[.,].*</(strong|STRONG)>',r') ',texte)        
            #enlève les insécables et met les sauts de lignes
            texte = re.sub('&nbsp;', ' ', texte)
            texte = re.sub('<br>\s*', '\n\n', texte)
            texte = re.sub('<BR>\s*', '\n\n', texte)
            #nettoie les balises qui restent
            self.donnees['question'] = re.sub('<.*?>', '', texte)
            self.donnees['ASREP'] = "Sans réponse"
        else:
            #sépare texte 
            texte= re.split('<TEXTES>',buf)
            texte = re.split('</TEXTES>',texte[1])
            #récupère la question et la nettoie des balises
            texte = re.split('<QUEST>',texte[0])
            texte = re.split('</QUEST>',texte[1])
            self.donnees['question'] = re.sub('<.*?>', '', texte[0])
            #récupère la réponse si besoin et la nettoie
            if (self.donnees['ASREP'] == "Avec réponse") :
                if (re.search("<REP>",  texte[1])):
                    texte = re.split('<REP>', texte[1])
                else:
                    texte = re.split('<U>Texte de la REPONSE : </U>', texte[1])
                texte = re.subn('&nbsp;', ' ', texte[1])                                        
                reponse = re.sub('<br>\s*', '\n\n', texte[0])
                reponse = re.sub('<BR>\s*', '\n\n', reponse)
                #Le titre
                reponse = re.sub('</a></p>','\n.',reponse)
                #Les locuteurs -----------------------
                reponse = re.sub(' *<(strong|STRONG)>\s*(.*)[.,]</(strong|STRONG)',r'(LOC \2)<',reponse)
                self.donnees['reponse'] = re.sub('<.*?>', '', reponse)
        
class EcritFichiers(object):
    "Ecrit un fichier pour prospero."

    def __init__(self,leg,num,extension):
        #nom de fichier complété par des zéros au besoin
        nom_court = "QPno%s_%s" % (leg,'0' * (6 - len(num)) + num)
        self.nom_fichier = "%s.%s" % (nom_court,extension)
        self.nom_rep = "%sREP.%s" % (nom_court,extension)
        
    def fin_de_ligne (self,ligne):
        ligne += "\n"
        try :
            return  ligne.encode('latin1',errors='xmlcharrefreplace')
        except:
            return ligne

    def ecrit(self,cible,contenu_fichier,REP=0):
        if (REP == 1) :
            nom = self.nom_rep
        else :
            nom = self.nom_fichier
        if (verbose):
            print nom
        pointeur_fichier = open(os.path.join(cible,nom),'w')
        if (verbose):
            print "mapping"
        texte_fichier = map(self.fin_de_ligne,contenu_fichier)
        if (verbose):
            print "writing"
            print texte_fichier
        pointeur_fichier.writelines(texte_fichier)
        if (verbose):
            print "closing"
        pointeur_fichier.close()
        return nom



def recherche(mot_clefs,de,au,leg):
    assemblee = []
    senat = []
    assembleeLiens =[]
    senatLiens = []
    if (leg):
        ASS = fouilleASS(mot_clefs,leg)
        assemblee = ASS.listeASS
        assembleeLiens = ASS.listeLiens
    if (de != au):
        SENAT = fouilleSENAT(mot_clefs,de,au)
        senat = SENAT.listeSENAT
        senatLiens = SENAT.listeLiens
    return assemblee,assembleeLiens,senat,senatLiens
       

def traite(question, cible, final):
	
    if (verbose): print question
    listeFichiers = []
    #cible = cible.encode('latin1','strict') #don't remember why this, but it fails on accentuated directory names

    if ((question != "SENAT") and (question != "ASSEMBLEE")):
        if (re.search("http://questions.assemblee-nationale.fr", question)):
            if (verbose): print "Traite assemblee",
            buf = urllib.urlopen(question).read()
            if re.search('<LEG>',buf):
                if (verbose): print " 1",
                DATA =  parseASS(buf).donnees
            elif re.search("question_legislature", buf):
                if (verbose): print " 3"
                DATA =  parseASS3(buf).donnees
            else :
                if (verbose): print " 2",
                DATA =  parseASS2(buf).donnees
            if (verbose): print " ok"                
        else:
            if (verbose): print "Traite Senat"
            if re.search('http://www.senat.fr/basile/visio.do', question):
                url = question
            else:
                url = "http://www.senat.fr/basile/visio.do?id=%s" % question
            if (verbose): print url
            buf = urllib.urlopen(url).read()
            DATA = parseSENAT(buf).donnees
            if (verbose): print " ok"  
  
        #--    CREATION DES FICHIERS           

       
        if (DATA['pgq']):
            titre = u"%s n°%s, publiée au JO le %s (page %s)" % (DATA['nature'],DATA['num'],DATA['dpq'],DATA['pgq'])
        else :
            titre = u"%s n°%s, publiée au JO le %s" % (DATA['nature'],DATA['num'],DATA['dpq'])
        titre = re.sub('\s{1,}',' ',titre)
        if (verbose):
            print titre

        if (verbose) :
            print "-------------" 
            print DATA
            print "-------------" 

        monTXT = EcritFichiers(DATA['leg'],DATA['num'],'txt')
        nameFichier = monTXT.ecrit(cible,[titre,".","",DATA['question']])
        listeFichiers.append(nameFichier)
        monCTX = EcritFichiers(DATA['leg'],DATA['num'],'ctx')

        if (verbose) : print "je passe au CTX"
	
        texteCTX = [
            "fileCtx0005",
            titre,
            DATA['aut'],
            DATA['groupe'],
            DATA['ministere'],
            DATA['dpq'],
            "Journal Officiel",
            "Question parlementaire",
            DATA['ASREP'],
            "Parlementaires",
            DATA['dept'],
            "Question parlementaire",
            "",
            "n",
            "n",
            "REF_HEURE:00:00"
            ]

        texteCTX = map(lambda x : re.sub('\s{1,}',' ',x),texteCTX)
            
        if (DATA['ASREP'] == "Avec réponse"): texteCTX.append("REF_EXT:%s\%s" % (final,monTXT.nom_rep))

        if (verbose) :  print "j'ecris le CTX"
        listeFichiers.append(monCTX.ecrit(cible,texteCTX))
        
        if (verbose) :  print "je passe au CTX de la reponse"
        #s'il y a une réponse
        if (DATA['ASREP'] == "Avec réponse") :
            
            TexteTXREP = [u"Réponse à la %s" % titre,".","",DATA['reponse']]
            listeFichiers.append(monTXT.ecrit(cible,TexteTXREP,1))

            
            TexteCTXREP = [
            u"fileCtx0005",
            u"Réponse à la %s" % titre,
            DATA['ministere'],
            "",
            DATA['aut'],
            DATA['dpr'],
            u"Journal Officiel",
            u"Réponse à une question parlementaire",
            "",
            u"Ministère",
            "",
            u"Réponse à une question parlementaire",
            "",
            u"n",
            u"n",
            u"REF_HEURE:00:00",
            u"REF_EXT:%s\%s" % (final,monTXT.nom_fichier)
            ]

            if (verbose) : print "j'ecris le CTX"

            TexteCTXREP = map(lambda x : re.sub('\s{1,}',' ',x),TexteCTXREP)

            tempName = monCTX.ecrit(cible,TexteCTXREP,1)
            listeFichiers.append(tempName)

        return listeFichiers



if __name__ == "__main__":
    url  = raw_input("L'adresse de votre question ")
    if (url):
        listeFichiers = traite(url,".",".")
        print (u"J'ai généré %d fichiers : %s" %( len(listeFichiers) , ", ".join(listeFichiers)))
    

