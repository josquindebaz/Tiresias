# -*- coding: utf-8 -*-
# Tiresias Desktop
version = "29/10/2018"
# Author Josquin Debaz
# GNU General Public License
# Version 3, 29 June 2007
# See http://www.gnu.org/licenses/ or COPYING.txt for more information.

## Modules python
import re
import os
import Tkinter
import tkFileDialog
import time
import webbrowser
import urllib
import string
## Modules Tirésias
import text_cleaner
import factiva
import qp
import Europresse_HTML
import carteqp
import lexis

class simpleapp_tk(Tkinter.Tk):
        
        def __init__(self,parent):
                Tkinter.Tk.__init__(self,parent)
                self.parent = parent
                self.title(u"Tirésias Desktop version %s"%version)
                self.initialize()



        def accueille(self):
                self.geometry("465x280")
                for item in self.grid_slaves():
                        item.destroy()
                self.vAccueil = Tkinter.StringVar()
                self.vAccueil = """
Bienvenue sur Tirésias Desktop

Logiciel conçu par Josquin Debaz pour l'association Doxa
http://prosperologie.org

Version du %s

Remarques, commentaires et suggestions sur 
http://prosperologie.org/forum

Script pour Europresse initié par Guillaume Ollivier

Merci à Robin, Federico, Guillaume, Markku, Patrick, Pierrick et Thomas pour les suggestions et retours de bug

"""%version
                accueil = Tkinter.Message(bg="white",fg="black",width=460,relief="groove",justify="center",text=self.vAccueil)
                accueil.grid(row=1,column=1)
                
        def initialize(self):
                self.grid()
                self.accueille()

                

                #les menus
                menu = Tkinter.Menu(self)
                
                # Création du menu fichiers:
                fichier = Tkinter.Menu(menu, tearoff=0)
                menu.add_cascade(label="Fichiers",menu=fichier)
                fichier.add_command(label="Lister les .txt d'un répertoire",command=self.liste_textes)
                fichier.add_command(label="Supprimer les .bdt d'un répertoire", command=self.delBDT)
                fichier.add_command(label="Version", command=self.accueille)
                fichier.add_command(label="Quitter", command=self.quit)

                # Création du menu correcteurs:
                correcteurs = Tkinter.Menu(menu, tearoff=0)
                menu.add_cascade(label="Correcteurs",menu=correcteurs)
                correcteurs.add_command(label="Nettoyage de caractères (Prospéro 1 en français)", command=self.nettoie)
                correcteurs.add_command(label="Traitement des groupes de capitales",command=self.gestion_majuscules)
                correcteurs.add_command(label="Correcteur de mots ", command=self.corr_mots)

                # création modif corpus:
                modif =  Tkinter.Menu(menu, tearoff=0)
                menu.add_cascade(label="Modification prc",menu=modif)
                modif.add_command(label="Change lettre du disque prc/ctx", command=self.change_lettre)
                modif.add_command(label="Filtreur", command=self.Filtreur)
             
                # Création du menu bases de données:
                bases= Tkinter.Menu(menu, tearoff=0)
                menu.add_cascade(label="Bases de données",menu=bases)
                bases.add_command(label="Questions parlementaires", command=self.questionsParlementaires)
                bases.add_command(label="Factiva", command=self.factiva)
                bases.add_command(label="Europresse", command=self.europresse)
                bases.add_command(label="Lexis Nexis", command=self.lexis)
                bases.add_command(label="Télécharger le support.publi", command=self.recup_support)

                # Création du menu traitements:
                traitements= Tkinter.Menu(menu, tearoff=0)
                menu.add_cascade(label="Traitements",menu=traitements)
                traitements.add_command(label="Années citées", state="active", command=self.annees_citees)
                traitements.add_command(label="Carte des départements", command=self.carteqp)

                #affiche le menu
                self.config(menu=menu)

                


        def progress_bar(self):
                self.fenetre_barre = Tkinter.Toplevel()
                self.fenetre_barre.geometry("550x50")
                self.fenetre_barre.title("barre de progression")
                self.barre = Tkinter.Canvas(self.fenetre_barre,width=510,height=50)
                self.barre.create_rectangle(5,15,505,35,fill="white")
                self.barre.grid(column=1,row=1,sticky='NW')
                self.v = Tkinter.StringVar()
                self.v.set("0%")
                pourcent = Tkinter.Label(self.fenetre_barre,textvariable=self.v)
                pourcent.grid(column=2,row=1)
                                
        def progress_bar_avance(self,indice):
                self.barre.create_rectangle(5,18,indice*5+5,32,fill="light blue")
                self.barre.update()
                self.v.set(str(indice)+" %")
                if indice >= 100:
                        self.fenetre_barre.destroy()

        def sel_dir(self):
                self.entry_rep.delete(0,"end")
                rep = tkFileDialog.askdirectory(title=u"sélectionner votre répertoire")
                self.entry_rep.insert(0,rep)



## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 
## Menu Fichiers
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 

##############################################################
## liste les .txt d'un dossier et de ses sous-dossiers
###############################################################
                
        def liste_textes(self):
                self.geometry("700x500")
                for item in self.grid_slaves():
                        item.destroy()
                self.LT_entry = Tkinter.Entry(self,width=60)
                self.LT_entry.grid(column=1,row=1,columnspan=2,sticky='NW')                
                bouton1 = Tkinter.Button(self, text=u"choisir le répertoire", command= self.LT_sel_dir)
                bouton1.grid(column=3,row=1,sticky='NW')
                bouton2 = Tkinter.Button(self, text=u"lister les .txt", command= self.LT_liste_dir)
                bouton2.grid(column=1,row=2,sticky='NW')
                bouton3 = Tkinter.Button(self, text=u"copier la liste", command= self.LT_copier)
                bouton3.grid(column=2,row=2,sticky='NW')
                self.LT_ZONEtexte = Tkinter.Text(self)
                self.LT_ZONEtexte.grid(column=1,row=3,columnspan=3,sticky='NSEW')
                ascenseur= Tkinter.Scrollbar(self)
                ascenseur.grid(column=4,row=3,sticky='NSEW')
                ascenseur.configure(command=self.LT_ZONEtexte.yview)
                self.LT_ZONEtexte.configure(yscrollcommand=ascenseur.set)
                self.LT_resultat = Tkinter.Label(self,text="Liste les .txt et les .TXT d'un répertoire et de ses sous-répertoires récursivement")
                self.LT_resultat.grid(column=1,row=4,columnspan=4,sticky='NSEW')

        def LT_sel_dir(self):
                self.LT_entry.delete(0,"end")
                self.LT_ZONEtexte.delete(1.0,"end")
                sel_dir = tkFileDialog.askdirectory(title=u"sélectionner votre répertoire")
                self.LT_entry.insert(0,sel_dir)

        def LT_liste_dir(self):
                self.LT_ZONEtexte.delete(1.0,"end")
                listeTXT = text_cleaner.liste_TXT(self.LT_entry.get())
                for F in listeTXT.lesTXT:
                        self.LT_ZONEtexte.insert("end","%s\n"%F)
                self.LT_resultat.config(text="%d .txt trouvé(s)" % len(listeTXT.lesTXT))

        def LT_copier(self):
                BUF =  self.LT_ZONEtexte.get(1.0,"end")
                self.LT_ZONEtexte.clipboard_clear()
                self.LT_ZONEtexte.clipboard_append(BUF)


##############################################################
## efface les .bdt d'un dossier et de ses sous-dossiers
###############################################################
                
        def delBDT(self):
                self.geometry("700x500")
                for item in self.grid_slaves():
                        item.destroy()
                self.LT_entry = Tkinter.Entry(self,width=60)
                self.LT_entry.grid(column=1,row=1,columnspan=2,sticky='NW')                
                bouton1 = Tkinter.Button(self, text=u"choisir le répertoire", command= self.listeBDT_sel_dir)
                bouton1.grid(column=3,row=1,sticky='NW')
                bouton2 = Tkinter.Button(self, text=u"lister les .bdt", command= self.listeBDT_dir)
                bouton2.grid(column=1,row=2,sticky='NW')
                self.bouton3 = Tkinter.Button(self, text=u"effacer les .bdt", command= self.listeBDT_remove, state=Tkinter.DISABLED)
                self.bouton3.grid(column=2,row=2,sticky='NW')
                self.LT_ZONEtexte = Tkinter.Text(self)
                self.LT_ZONEtexte.grid(column=1,row=3,columnspan=3,sticky='NSEW')
                ascenseur= Tkinter.Scrollbar(self)
                ascenseur.grid(column=4,row=3,sticky='NSEW')
                ascenseur.configure(command=self.LT_ZONEtexte.yview)
                self.LT_ZONEtexte.configure(yscrollcommand=ascenseur.set)
                self.LT_resultat = Tkinter.Label(self,text=u"choisissez votre répertoire")
                self.LT_resultat.grid(column=1,row=4,columnspan=4,sticky='NSEW')
                self.LT_resultat = Tkinter.Label(self,text="Supprime les .bdt et les .BDT d'un répertoire et de ses sous-répertoires récursivement")
                self.LT_resultat.grid(column=1,row=4,columnspan=4,sticky='NSEW')
                
        def listeBDT_sel_dir(self):
                self.LT_entry.delete(0,"end")
                self.LT_ZONEtexte.delete(1.0,"end")
                sel_dir = tkFileDialog.askdirectory(title="sélectionner votre répertoire")
                self.LT_entry.insert(0,sel_dir)
                self.bouton3.config(state=Tkinter.DISABLED)

        def listeBDT_dir(self):
                self.LT_ZONEtexte.delete(1.0,"end")
                rep = self.LT_entry.get()
                self.lesBDT = []
                if (rep):
                        for roots,dirs,files in os.walk(rep):
                                for f in files :
                                    if ((os.path.splitext(f)[1] == '.bdt') or (os.path.splitext(f)[1] == '.BDT')):
                                            self.lesBDT.append(os.path.join(roots,f))
                        for F in self.lesBDT:
                                self.LT_ZONEtexte.insert("end","%s\n"%F)
                        self.LT_resultat.config(text="%d .bdt trouvé(s)" % len(self.lesBDT))
                        self.bouton3.config(state=Tkinter.ACTIVE)

        def listeBDT_remove(self):
                for F in  self.lesBDT:
                        os.unlink(F)
                self.LT_resultat.config(text=".bdt effacés")





## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 
## Menu Correcteurs
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 


##############################################################
## module qui nettoie les caractères spéciaux des .txt d'un dossier et de ses sous-dossiers

        def nettoie(self):
                """nettoie les caractères spéciaux des .txt d'un dossier et de ses sous-dossiers"""
                self.geometry("700x500")
                for item in self.grid_slaves():
                        item.destroy()
                self.nettoie_entry = Tkinter.Entry(self,width=60)
                self.nettoie_entry.grid(column=1,row=1,columnspan=2,sticky='NW')                
                bouton1 = Tkinter.Button(self, text=u"choisir le répertoire", command= self.nettoie_sel_dir)
                bouton1.grid(column=3,row=1,sticky='NW')
                bouton2 = Tkinter.Button(self, text=u"nettoyer les .txt", command= self.nettoie_liste_dir)
                bouton2.grid(column=1,row=2,sticky='NW')
                self.nettoie_ZONEtexte = Tkinter.Text(self)
                self.nettoie_ZONEtexte.grid(column=1,row=3,columnspan=3,sticky='NSEW')
                ascenseur= Tkinter.Scrollbar(self)
                ascenseur.grid(column=4,row=3,sticky='NSEW')
                ascenseur.configure(command=self.nettoie_ZONEtexte.yview)
                self.nettoie_ZONEtexte.configure(yscrollcommand=ascenseur.set)
                self.nettoie_resultat = Tkinter.Label(self,text="choissisez votre répertoire")
                self.nettoie_resultat.grid(column=1,row=4,columnspan=4,sticky='NSEW')

        def nettoie_sel_dir(self):
                self.nettoie_entry.delete(0,"end")
                self.nettoie_ZONEtexte.delete(1.0,"end")
                sel_dir = tkFileDialog.askdirectory(title="sélectionner votre répertoire")
                self.nettoie_entry.insert(0,sel_dir)
                self.nettoie_resultat.config(text="lancez le traitement en cliquant sur nettoyer les .txt")

        def nettoie_liste_dir(self):
                self.nettoie_ZONEtexte.delete(1.0,"end")
                listeTXT = text_cleaner.liste_TXT(self.nettoie_entry.get())
                compteur = [0,0]
                self.progress_bar()
                progress = 0 
                for TXT in listeTXT.lesTXT:
                        le_fichier = text_cleaner.agit_dans_un_fichier(TXT)
                        le_nettoyeur = text_cleaner.agent_de_surface(le_fichier.buf)
                        le_fichier.corrige(le_nettoyeur.BUF)
                        if le_nettoyeur.compte_modif:
                                self.nettoie_ZONEtexte.insert("1.0","J'ai fait %d correction(s) sur le fichier %s\n"%(le_nettoyeur.compte_modif,TXT))
                                self.nettoie_ZONEtexte.update()
                                compteur[0] += 1
                                compteur[1] += le_nettoyeur.compte_modif
                        progress += 1
                        self.progress_bar_avance(progress*100/len(listeTXT.lesTXT))
                        
                self.fenetre_barre.destroy()
                self.nettoie_resultat.config(text="%d .txt traité(s), %d correction(s)" % (compteur[0], compteur[1]))

                
##############################################################
## module qui permet de transformer la casse dans les textes d'un dossier et de ses sous-dossiers            

        def gestion_majuscules(self):
                self.geometry("680x700")
                for item in self.grid_slaves():
                        item.destroy()
                #row 1
                self.GM_entry = Tkinter.Entry(self)
                self.GM_entry.grid(column=2,row=1,columnspan=5,sticky='NEW')
                bouton1 = Tkinter.Button(self, text=u"choisir le répertoire", command= self.GM_sel_dir)
                bouton1.grid(column=1,row=1,sticky='NEW')
                #row 2
                self.labelmin = Tkinter.Label(self,text="minimum")
                self.labelmin.grid(column=1,row=2,sticky='NE')
                self.GM_min = Tkinter.Entry(self)
                self.GM_min.grid(column=2,row=2,sticky='NW')
                self.GM_min.insert(0,"3")
                self.labelmax = Tkinter.Label(self,text="maximum")
                self.labelmax.grid(column=4,row=2,sticky='NE')
                self.GM_max = Tkinter.Entry(self)
                self.GM_max.grid(column=5,row=2,sticky='NW')
                self.GM_max.insert(0,"100")
                #row 3
                bouton2 = Tkinter.Button(self, text=u"lister les groupes de majuscules", command= self.GM_liste_dir)
                bouton2.grid(column=1,row=3,sticky='NW')
                bouton4 = Tkinter.Button(self, text=u"capitaliser", command = self.GM_capit)
                bouton4.grid(column=4,row=3,sticky='NW')
                bouton5 = Tkinter.Button(self, text=u"minusculiser", command = self.GM_minusc)
                bouton5.grid(column=5,row=3,sticky='NW')
                #row 4
                self.GM_ZONEtexte = Tkinter.Listbox(self,width=50,height=25)
                self.GM_ZONEtexte.grid(column=1,row=4,columnspan=2,sticky='NSEW')
                self.GM_ZONEtexte.bind('<ButtonRelease-1>', self.GM_clicG)
                ascenseur= Tkinter.Scrollbar(self)
                ascenseur.grid(column=3,row=4,sticky='NSEW')
                ascenseur.configure(command=self.GM_ZONEtexte.yview)
                self.GM_ZONEtexte.configure(yscrollcommand=ascenseur.set)
                self.GM_ZONEtexte2 = Tkinter.Listbox(self,width=50,height=25)
                self.GM_ZONEtexte2.grid(column=4,row=4,columnspan=2,sticky='NSEW')
                self.GM_ZONEtexte2.bind('<ButtonRelease-1>', self.GM_clicD)
                ascenseur2= Tkinter.Scrollbar(self)
                ascenseur2.grid(column=6,row=4,sticky='NSEW')
                ascenseur2.configure(command=self.GM_ZONEtexte2.yview)
                self.GM_ZONEtexte2.configure(yscrollcommand=ascenseur2.set)
                #row 5
                self.GM_ZONEtexte3 = Tkinter.Text(self,height="12")
                self.GM_ZONEtexte3.grid(column=1,row=5,columnspan=5,sticky='NEW')  
                ascenseur3= Tkinter.Scrollbar(self)
                ascenseur3.grid(column=6,row=5,sticky='NSEW')
                ascenseur3.configure(command=self.GM_ZONEtexte3.yview)
                self.GM_ZONEtexte3.configure(yscrollcommand=ascenseur3.set)
                self.GM_ZONEtexte3.insert("1.0",u"Choisissez votre répertoire\n")

        def GM_sel_dir(self):
                self.GM_entry.delete(0,"end")
                self.GM_ZONEtexte.delete(0,"end")
                sel_dir = tkFileDialog.askdirectory(title="sélectionner un répertoire")
                self.GM_entry.insert(0,sel_dir)
                self.GM_ZONEtexte3.insert("1.0","lancez la recherche en cliquant sur lister les groupes de majuscules\n")

        def GM_liste_dir(self):
                self.GM_ZONEtexte.delete(0,"end")
                compteur = 0
                liste_maj = []
                listeTXT = text_cleaner.liste_TXT(self.GM_entry.get())
                for F in listeTXT.lesTXT:
                        BUF = open(F,'r').read()
                        for match in  re.findall(u"[A-ZÉÈÜÄËÖÊ\-]{%d,%d}"%(int(self.GM_min.get()),int(self.GM_max.get())),BUF):
                                if not (match in liste_maj):
                                        liste_maj.append(match)
                                        compteur += 1

                if (len(liste_maj) > 0):
                        for M in sorted(liste_maj):
                                self.GM_ZONEtexte.insert("end","%s"%M)
                                
                self.GM_ZONEtexte3.insert("1.0","%d groupe(s) de majuscules trouvé(s)\n" % compteur)

        def GM_copier(self):
                BUF =  self.GM_ZONEtexte.get(0,"end")
                self.GM_ZONEtexte.clipboard_clear()
                self.GM_ZONEtexte.clipboard_append(BUF)

        def GM_clicG(self,inutile):
                select =  self.GM_ZONEtexte.curselection()
                self.GM_ZONEtexte2.insert("end",self.GM_ZONEtexte.get(select)) #ne pas inverser surtout
                self.GM_ZONEtexte.delete(select)

        def GM_clicD(self,inutile):
                select =  self.GM_ZONEtexte2.curselection()
                self.GM_ZONEtexte.insert("end",self.GM_ZONEtexte2.get(select)) #ne pas inverser surtout
                self.GM_ZONEtexte2.delete(select)

        def GM_capit_minus(self,roots,files,motifs,action):
                for f in files :
                            if (os.path.splitext(f)[1] == '.txt'):
                                    BUF = open(os.path.join(roots,f),'r').read()
                                    cpt = 0
                                    for M in motifs:
##                                            M = M[0:-1]         #enlève le \n final
                                            if (re.search(M,BUF)):
                                                    if (action == "capitalize"):
                                                            neo = "-".join(map(lambda x : x.capitalize(),M.split("-")))
                                                            neo = re.sub("(\S)É","\\1é",neo)
                                                            neo = re.sub("(\S)È","\\1è",neo)
                                                            neo = re.sub("(\S)Ü","\\1ü",neo)
                                                            neo = re.sub("(\S)Ä","\\1ä",neo)
                                                            neo = re.sub("(\S)Ë","\\1ë",neo)
                                                            neo = re.sub("(\S)Ö","\\1ö",neo)
                                                            neo = re.sub("(\S)Ê","\\1ê",neo)
                                                    elif (action == "lower"):
                                                            neo = M.lower()
                                                            neo = re.sub("É","é",neo)
                                                            neo = re.sub("È","è",neo)
                                                            neo = re.sub("Ü","ü",neo)
                                                            neo = re.sub("Ä","ä",neo)
                                                            neo = re.sub("Ë","ë",neo)
                                                            neo = re.sub("(\S)Ö","\\1ö",neo)
                                                            neo = re.sub("(\S)Ê","\\1ê",neo)
                                                    BUF = re.sub(M,neo,BUF)                                                
                                                    cpt += 1
                                    if (cpt):
                                            self.GM_ZONEtexte3.insert("1.0", "%d modifications sur le fichier %s\n" % (cpt,f))
                                            FILE =  open(os.path.join(roots,f),'w')
                                            FILE.write(BUF)
                                            FILE.close()
                                            
        def GM_capit(self):
                motifs = self.GM_ZONEtexte2.get(0,"end")
                for roots,dirs,files in os.walk(self.GM_entry.get()):
                        self.GM_capit_minus(roots,files,motifs,"capitalize")
                self.GM_ZONEtexte2.delete(0,"end")

        def GM_minusc(self):
                motifs = self.GM_ZONEtexte2.get(0,"end")
                for roots,dirs,files in os.walk(self.GM_entry.get()):
                        self.GM_capit_minus(roots,files,motifs,"lower")
                self.GM_ZONEtexte2.delete(0,"end")


##############################################################
## module qui permet de corriger des mots

        def corr_mots(self):
                """corrige des mots dans les .txt d'un dossier et de ses sous-dossiers"""
                self.geometry("700x850")
                for item in self.grid_slaves():
                        item.destroy()
                #row 1
                bouton6 = Tkinter.Button(self, text=u"traiter le répertoire",command=self.CM_lanceur)
                bouton6.grid(column=1,columnspan=2,row=1,sticky='NSW')
                bouton1 = Tkinter.Button(self, text=u"choisir le répertoire", command= self.CM_sel_dir)
                bouton1.grid(column=3,row=1,sticky='NSE')
                self.CM_entry = Tkinter.Entry(self)
                self.CM_entry.grid(column=4,columnspan=5,row=1,sticky='NSEW')
                
                #row 2
                bouton21 = Tkinter.Button(self, text=u"fichier de configuration", command= self.CM_sel_conf)
                bouton21.grid(column=1,row=2,sticky='NSEW')
                self.configEntry=Tkinter.Entry(self)
                self.configEntry.grid(column=2,columnspan=5,row=2,sticky='NSEW')
                bouton22 = Tkinter.Button(self, text=u"enregistrer",command= self.CM_sav_config)
                bouton22.grid(column=6,columnspan=3,row=2,sticky='NSE')
 
                #row 3
                labl31 = Tkinter.Label(self,text="formes correctes",fg="green",font=("Helvetica", 10))
                labl31.grid(column=1,columnspan=3,row=3,sticky='NSEW')
                labl32 = Tkinter.Label(self,text="formes à corriger",fg="red",font=("Helvetica", 10))
                labl32.grid(column=4,columnspan=3,row=3,sticky='NSEW')
                
                #row 4                        
                self.listeboxG = Tkinter.Listbox(self,height=20,width=40,selectbackground="green")
                self.listeboxG.grid(column=1,columnspan=3,row=4,sticky="NSEW")
                ascenseurG= Tkinter.Scrollbar(self)
                ascenseurG.grid(column=3,row=4,sticky='NSEW')
                ascenseurG.configure(command=self.listeboxG.yview)
                self.listeboxG.configure(yscrollcommand=ascenseurG.set)
                self.listeboxG.bind('<ButtonRelease-1>', self.CM_clicGG)
                self.listeboxG.bind('<ButtonRelease-3>', self.CM_clicDG)

                self.listeboxD = Tkinter.Listbox(self,height=20,width='40',selectbackground="red")
                self.listeboxD.grid(column=4,columnspan=3,row=4,sticky='NSEW')
                ascenseurD= Tkinter.Scrollbar(self)
                ascenseurD.grid(column=8,row=4,sticky='NSEW')
                ascenseurD.configure(command=self.listeboxD.yview)
                self.listeboxD.configure(yscrollcommand=ascenseurD.set)
                self.listeboxD.bind('<ButtonRelease-1>', self.CM_clicGD)
                self.listeboxD.bind('<ButtonRelease-3>', self.CM_clicDD)
                        
                #row 5
                self.Gentry = Tkinter.Entry(self)
                self.Gentry.grid(column=1,columnspan=3,row=5,sticky='NSEW')
                self.bouton5Gplus = Tkinter.Button(self, text=u"+",command=self.add_correcte)
                self.bouton5Gplus.grid(column=3,row=5,sticky='NSE')
                self.Dentry = Tkinter.Entry(self)
                self.Dentry.grid(column=4,columnspan=3,row=5,sticky='NSEW')

                #row 6
                self.CM_ZONEtexte = Tkinter.Text(self)
                self.CM_ZONEtexte.grid(column=1,row=6,columnspan=6,sticky='NSEW')
                ascenseurZT= Tkinter.Scrollbar(self)
                ascenseurZT.grid(column=8,row=6,sticky='NSEW')
                ascenseurZT.configure(command=self.CM_ZONEtexte.yview)
                self.CM_ZONEtexte.configure(yscrollcommand=ascenseurZT.set)

                #charge la config par défaut
                path = os.path.join(os.getcwd(), "corr_mots.cfg")
                if os.path.isfile(path):
                        self.configEntry.insert(0,path)
                        self.CM_recup_config(path)

        def CM_sel_dir(self):
                self.CM_entry.delete(0,"end")
                sel_dir = tkFileDialog.askdirectory(title="sélectionner un répertoire")
                self.CM_entry.insert(0,sel_dir)

        def CM_sel_conf(self):
                self.configEntry.delete(0,"end")
                sel_conf = tkFileDialog.askopenfilename(title="sélectionner un fichier")
                self.configEntry.insert(0,sel_conf)
                self.CM_recup_config(sel_conf)

        def CM_recup_config(self,path):
                self.corr_mots_config = {}
                for ligne in open(path,"r").readlines():
                        if not re.search("^\s*$",ligne):
                                l = re.split("\t",ligne)
                                l = map(lambda x :  re.sub("\n|\r","",x),l)
                                self.corr_mots_config [l[0]] = []
                                for i in l[1:]:
                                      if not re.search("^\s*$",i):
                                              self.corr_mots_config [l[0]] . append(i)
                if (hasattr(self, 'listeboxGactive')):
                        del self.listeboxGactive       
                self.CM_listG()
                self.listeboxD.delete(0,"end")

        def CM_sav_config(self):
                content = ""
                for k in self.corr_mots_config.keys():
                        content += "%s\t"%k
                        for i in self.corr_mots_config[k]:
                                content += "%s\t"%i        
                        content += "\n"
                fichier = tkFileDialog.asksaveasfile(mode='w', filetypes=[("","*.cfg")],defaultextension = ".cfg",initialfile="corr_mots.cfg")
                fichier.write(content)
                fichier.close()
                self.configEntry.delete(0,"end")
                self.configEntry.insert(0,os.path.abspath(fichier.name))

        def CM_listG(self):
                self.listeboxG.delete(0,"end")
                for i in self.corr_mots_config:
                        self.listeboxG.insert(Tkinter.END,i)
                if (hasattr(self, 'listeboxGactive')):
                        self.listeboxG.itemconfig(self.listeboxGactive, {'bg':'green',"fg":"white"})

        def CM_clicGG(self,event):
                self.bouton5Gplus.config(text="+",command=self.add_correcte)
                self.Gentry.delete(0,"end")
                self.Dentry.delete(0,"end")
                select =  self.listeboxG.curselection()
                self.listeboxGactive = select
                self.CM_listG()
                self.CM_listD(  self.listeboxG.get(select))
                self.bouton5Dplus = Tkinter.Button(self, text=u"+",command=self.add_a_cor)
                self.bouton5Dplus.grid(column=8,row=5,sticky='NSEW')

        def CM_clicDG(self,event):
                popupG = Tkinter.Menu(self, tearoff=0)
                if (hasattr(self, 'listeboxGactive')):
                        clef = self.listeboxG.get(self.listeboxGactive)
                        popupG.add_command(label="enlever %s" % (clef),command=self.del_correcte)
                        popupG.add_command(label="modifier %s" % (clef ),command=self.mod_correcte)               
                try:
                        popupG.tk_popup(event.x_root + 80, event.y_root + 20, 0)
                finally:
                        popupG.grab_release()

        def del_correcte(self):
                clef = self.listeboxG.get(self.listeboxGactive)
                del  self.corr_mots_config[clef]
                self.listeboxD.delete(0,"end")
                del self.listeboxGactive
                self.CM_listG()

        def add_correcte(self):
                ajout = self.Gentry.get()
                ajout = self.CM_latinise(ajout)
                if (ajout):
                        if not hasattr(self, 'corr_mots_config') :
                                self.corr_mots_config ={}                                
                        index = []
                        for l in self.corr_mots_config.values():
                                index.extend( l)
                        if ajout in self.corr_mots_config or ajout in index:
                                self.CM_ZONEtexte.insert("1.0", u"%s existe déjà\n"%ajout)
                        else:
                                self.corr_mots_config[ajout] = []
                                self.Gentry.delete(0,"end")
                                self.CM_listG()

        def mod_correcte(self):
                self.bouton5Gplus.config(text="M",command=self.mod_correcte_valid)
                self.Gentry.delete(0,"end")
                self.Gentry.insert(0,self.listeboxG.get(self.listeboxGactive))

        def mod_correcte_valid(self):
                mod = self.Gentry.get()
                mod = self.CM_latinise(mod)
                clef = self.listeboxG.get(self.listeboxGactive)
                if (mod):
                        index = []
                        for l in self.corr_mots_config.values():
                                index.extend( l)
                        if mod in index or mod in self.corr_mots_config:
                                self.CM_ZONEtexte.insert("1.0", u"%s existe déjà\n"%mod)
                        else:
                                self.corr_mots_config[mod] = self.corr_mots_config[clef]
                                del self.corr_mots_config[clef]
                                self.CM_listG()
                                self.bouton5Gplus.config(text="+",command=self.add_correcte)
                                self.Gentry.delete(0,"end")
                
        def CM_listD(self,clef):
                self.listeboxD.delete(0,"end")
                for i in self.corr_mots_config[clef]:
                        self.listeboxD.insert(Tkinter.END,i)

        def CM_clicGD(self,event):
                self.bouton5Dplus.config(text="+",command=self.add_a_cor)
                self.Dentry.delete(0,"end")
                self.bouton5Gplus.config(text="+",command=self.add_correcte)
                self.Gentry.delete(0,"end")
                
        def CM_clicDD(self,event):
                if (hasattr(self, 'listeboxGactive')):
                        popupD = Tkinter.Menu(self, tearoff=0)
                        clef = self.listeboxG.get(self.listeboxGactive)
                        
                        if (self.listeboxD.curselection()):
                                item = self.listeboxD.get(self.listeboxD.curselection())
                                popupD.add_command(label="enlever %s de %s" % (item, clef),command=self.del_a_corr )
                                popupD.add_command(label="modifier %s de %s" % (item, clef ),   command=self.mod_a_corr)
                        
                        try:
                                popupD.tk_popup(event.x_root + 80, event.y_root + 20, 0)
                        finally:
                                popupD.grab_release()
                      
        def del_a_corr(self):
                clef = self.listeboxG.get(self.listeboxGactive)
                enleve = self.listeboxD.curselection()
                self.corr_mots_config[clef].remove( self.listeboxD.get(enleve))
                self.CM_listD(clef)
               
        def add_a_cor(self):
                ajout = self.Dentry.get()
                ajout = self.CM_latinise(ajout)
                if( hasattr(self, 'listeboxGactive') and (ajout)):
                        clef = self.listeboxG.get(self.listeboxGactive)
                        index = []
                        for l in self.corr_mots_config.values():
                                index.extend( l)
                        if ajout in self.corr_mots_config or ajout in index:
                                self.CM_ZONEtexte.insert("1.0", u"%s existe déjà\n"%ajout)
                        else:
                                self.Dentry.delete(0,"end")
                                self.corr_mots_config[clef].append(ajout)
                                self.CM_listD(clef)
                                
        def mod_a_corr(self):
                self.bouton5Dplus.config(text="M",command=self.mod_a_corr_valid)
                self.Dentry.delete(0,"end")
                self.forme_a_corr_amod = self.listeboxD.get(self.listeboxD.curselection())
                self.Dentry.insert(0,self.forme_a_corr_amod)
                self.listeboxD.itemconfig(self.listeboxD.curselection(), {'bg':'red',"fg":"white"})

        def mod_a_corr_valid(self):
                mod = self.Dentry.get()
                mod = self.CM_latinise(mod)
                if (mod):
                        index = []
                        for l in self.corr_mots_config.values():
                                index.extend( l)
                        if mod in index or mod in self.corr_mots_config:
                                self.CM_ZONEtexte.insert("1.0", u"%s existe déjà\n"%mod)
                        else:
                                clef = self.listeboxG.get(self.listeboxGactive)
                                liste_clef = self.corr_mots_config[clef]
                                position = liste_clef.index(self.forme_a_corr_amod)
                                liste_clef[position] = mod
                                self.corr_mots_config[clef] = liste_clef
                                self.CM_listD(clef)
                                self.bouton5Dplus.config(text="+",command=self.add_a_cor)
                                self.Dentry.delete(0,"end")

        def CM_lanceur(self):
                if (self.CM_entry.get() != '') and   hasattr(self, 'corr_mots_config') :
                        index = []
                        for l in self.corr_mots_config.values():
                                index.extend( l)
                        AvAp = "[\s\.,;!\?\"']" #la liste des ponctuations et autres qui peuvent précéder ou suivre une forme à corriger
                        badindex =string.join(index,'|')
                        badindex = "(^|(%s))(%s)((%s)|$)" % (AvAp,badindex,AvAp)
                        badindex = re.compile(badindex)

                        self.progress_bar()
                        progress = 0

                        listeTXT = text_cleaner.liste_TXT(self.CM_entry.get())
                        cptfL = 0
                        cptfT = 0
                        for f in listeTXT.lesTXT:
                                progress += 1
                                self.progress_bar_avance(progress*100/len(listeTXT.lesTXT))
                                cptfL += 1
                                cpt = 0
                                BUF = open(f,'r').read()
                                while re.search(badindex,BUF):
                                        cpt += 1 #nombre de passages du correcteur
                                        for  good in self.corr_mots_config.keys():
                                                bad =string.join(self.corr_mots_config[good],'|')
                                                motif = "(^|(%s))(%s)((%s)|$)" % (AvAp,bad,AvAp)
                                                motif_compile = re.compile(motif)
                                                BUF = re.sub(motif_compile,"\\1%s\\4"%good,BUF)
                                if (cpt):
                                        try:
                                                self.CM_ZONEtexte.insert("1.0", u"Je modifie %s\n"%(f))
                                        except:
                                                self.CM_ZONEtexte.insert("1.0", u"Je modifie %s\n"%(u'%s'%f.decode('latin1')))
                                                
                                        cptfT += 1
                                        FILE =  open(f,'w')
                                        FILE.write(BUF)
                                        FILE.close()
                        self.CM_ZONEtexte.insert("1.0", u"%d fichier(s) traité(s), %d modifié(s)\n"%(cptfL,cptfT))

        def CM_latinise(self,chaine):
                if  isinstance(chaine, unicode):
                        return chaine.encode('latin1')
                else :
                        return chaine
                



## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 
## Menu modification corpus
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 


###############################################################
######## changer le répertoire des textes d'un corpus

        def change_lettre(self):
                for item in self.grid_slaves():
                        item.destroy()
                self.geometry("680x520")
                #row 1
                boutonPRC = Tkinter.Button(self, text=u"choisir le répertoire", command= self.sel_dir)
                boutonPRC.grid(column=1,row=1,sticky='NSEW')
                self.entry_rep = Tkinter.Entry(self,width=70)
                self.entry_rep.grid(column=2,row=1,sticky='NSEW')  
                #row 2
                self.CheckB_prc = Tkinter.IntVar()
                CL_prc = Tkinter.Checkbutton(text='PRC',variable=self.CheckB_prc)
                CL_prc.select() 
                CL_prc.grid(column=1,row=2,sticky='NW')
                self.CheckB_ctx = Tkinter.IntVar()
                CL_ctx = Tkinter.Checkbutton(text='CTX',variable=self.CheckB_ctx)
                CL_ctx.select() 
                CL_ctx.grid(column=2,row=2,sticky='NW')
                #row3
                
                CL_disque= Tkinter.Label(self,text="choisissez votre lettre de lecteur de disque")
                CL_disque.grid(column=2,row=3,sticky='NW')
                listeDisques = self.teste_disques()
                self.CL_entry_disque = Tkinter.Listbox(self,height=len(listeDisques))
                for disque in listeDisques:
                        self.CL_entry_disque.insert(Tkinter.END,disque)
                self.CL_entry_disque.grid(column=1,row=3,sticky='NW')
                #row4
                agit = Tkinter.Button(self, text=u"lancer le traitement", command= self.agit_CL)
                agit.grid(column=1,row=4,sticky='NSEW')
                #row4
                self.CL_ZONEtexte = Tkinter.Text(self)
                self.CL_ZONEtexte.grid(column=1,row=5,columnspan=3,sticky='NSEW')
                ascenseur= Tkinter.Scrollbar(self)
                ascenseur.grid(column=4,row=5,sticky='NSEW')
                ascenseur.configure(command=self.CL_ZONEtexte.yview)
                self.CL_ZONEtexte.configure(yscrollcommand=ascenseur.set)           

        def teste_disques(self):
                listeDisques = []
                for i in ["A","B","C","D","E"]:
                        if os.path.isdir("%s:\\"%i):
                                listeDisques.append(i)
                l = 70
                while (os.path.isdir("%s:\\"%chr(l))):
                        listeDisques.append(chr(l))
                        l+=1
                return listeDisques
               
                
        def agit_CL(self):
                if  self.CL_entry_disque.curselection():
                        lettreLecteur = self.CL_entry_disque.get(self.CL_entry_disque.curselection())
                        cPRC = [0,0]
                        cCTX = [0,0]
                        for roots,dirs,files in os.walk(self.entry_rep.get()):
                                for f in files:
                                        path = os.path.join(roots,f)
                                        if (self.CheckB_prc.get() and os.path.splitext(f)[1] in ['.prc',".PRC"]):
                                                BUF = open(path,'r').read()
                                                cPRC[0] += 1
                                                if re.search("[^%s]:"%lettreLecteur,BUF):
                                                        F = open(path,"w")
                                                        F.write(re.sub("\w:","%s:" % lettreLecteur,BUF))
                                                        F.close()
                                                        self.CL_ZONEtexte.insert(1.0,"%s  modifié\n"%f)
                                                        cPRC[1] += 1
                                                self.CL_ZONEtexte.update()
                                        if (self.CheckB_ctx.get() and os.path.splitext(f)[1] in ['.ctx',".CTX"]):
                                                cCTX[0] += 1
                                                BUF = open(path,'r').read()
                                                if re.search("REF_EXT:[^%s]:"%lettreLecteur,BUF):
                                                        F = open(path,"w")
                                                        F.write(re.sub("REF_EXT:\w:","REF_EXT:%s:" % lettreLecteur,BUF))
                                                        F.close()
                                                        self.CL_ZONEtexte.insert(1.0,"%s  modifié\n"%f)
                                                        cCTX[1] += 1
                                                self.CL_ZONEtexte.update()
                        self.CL_ZONEtexte.insert(1.0,"%d PRC lus, %d modifiés\n"%(cPRC[0],cPRC[1]))
                        self.CL_ZONEtexte.insert(1.0,"%d CTX lus, %d modifiés\n"%(cCTX[0],cCTX[1]))
                                                
                                        
###############################################################
######## Filtreur

        def Filtreur(self):
                for item in self.grid_slaves():
                        item.destroy()
                self.geometry("840x650")

                self.textesPRC = []
                
                #row 1
                boutonPRC = Tkinter.Button(self, text=u"choisir le projet", command= self.sel_PRC)
                boutonPRC.grid(column=1,columnspan=1,row=1,sticky='NSEW')
                self.entry_PRC = Tkinter.Entry(self,width=80)
                self.entry_PRC.grid(column=2,row=1,columnspan=6,sticky='NSEW')

                #row 2
                self.LB1txt = Tkinter.StringVar()
                LB1 = Tkinter.Label(self,textvariable=self.LB1txt)
                LB1.grid(column=1,row=2,columnspan=4,sticky='NSEW')
                LB2 = Tkinter.Label(self,text=u"thème")
                LB2.grid(column=6,columnspan=1,row=2,sticky='NSEW')
  
                #row 3-8
                self.ListeNEG = Tkinter.Listbox(self,width=105,height=15)
                self.ListeNEG.grid(column=1,columnspan=4,row=3,rowspan=5,sticky='NSEW')
                ascenseurListeNEG = Tkinter.Scrollbar(self)
                ascenseurListeNEG.grid(column=5,row=3,rowspan=5,sticky='NSEW')
                ascenseurListeNEG.configure(command=self.ListeNEG.yview)
                self.ListeNEG.configure(yscrollcommand=ascenseurListeNEG.set)
                ascenseurHListeNEG= Tkinter.Scrollbar(self,orient=Tkinter.HORIZONTAL)
                ascenseurHListeNEG.grid(column=1,row=8,columnspan=4,sticky='NSEW')
                ascenseurHListeNEG.configure(command=self.ListeNEG.xview)
                self.ListeNEG.configure(xscrollcommand=ascenseurHListeNEG.set)
                
                self.ListeNEG.bind('<Double-Button-1>',self.ListeNEGdoubleclic)

                self.ListeDef = Tkinter.Listbox(self)
                self.ListeDef.grid(column=6,columnspan=1,row=3,rowspan=5,sticky='NSEW')

                BTplus = Tkinter.Button(self, text=u"ajouter",command=self.filtreurAdd)
                BTplus.grid(column=7,row=3,sticky='NWE')
                BTmoins = Tkinter.Button(self, text=u"effacer",command=self.filtreurRem)
                BTmoins.grid(column=7,row=4,sticky='NWE')

                BTsave = Tkinter.Button(self, text=u"sauver",command=self.filtreur_sav_config)
                BTsave.grid(column=7,row=5,sticky='NWE')
                BTload= Tkinter.Button(self, text=u"charger",command=self.filtreur_sel_conf)
                BTload.grid(column=7,row=6,sticky='NWE')              


                #charge la config par défaut
##                path = os.path.join(os.getcwd(), "filtreur.cfg")
##                if os.path.isfile(path):
##                        self.filtreur_recup_config(path)

                #row 9
                LB3 = Tkinter.Label(self,text=u"score >=",justify=Tkinter.RIGHT)
                LB3.grid(column=1,columnspan=1,row=9,sticky='NSEW')
                self.entry_Score = Tkinter.Entry(self,width=5)
                self.entry_Score.grid(column=2,columnspan=1,row=9,sticky='NSW')
                self.entry_Score.insert(0,"4")
                LB4 = Tkinter.Label(self,text=u"deploiement >=",justify=Tkinter.RIGHT)
                LB4.grid(column=3,columnspan=1,row=9,sticky='NSEW')
                self.entry_Dep = Tkinter.Entry(self,width=5)
                self.entry_Dep.grid(column=4,columnspan=1,row=9,sticky='NSW')
                self.entry_Dep.insert(0,"2")
                boutonEval = Tkinter.Button(self, text=u"évaluer",command=self.FiltreurEval)
                boutonEval.grid(column=6,columnspan=1,row=9,sticky='NSEW')
                
                #row 10
                self.LB5txt = Tkinter.StringVar()
                LB5 = Tkinter.Label(self,textvariable=self.LB5txt)
                LB5.grid(column=1,row=10,columnspan=4,sticky='NSEW')
                
                #row 11-13
                self.ListePOS = Tkinter.Listbox(self,height=15)
                self.ListePOS.grid(column=1,columnspan=4,row=11,rowspan=2,sticky='NSEW')
                ascenseurListePOS = Tkinter.Scrollbar(self)
                ascenseurListePOS.grid(column=5,row=11,rowspan=2,sticky='NSEW')
                ascenseurListePOS.configure(command=self.ListePOS.yview)
                self.ListePOS.configure(yscrollcommand=ascenseurListePOS.set)
                ascenseurHListePOS= Tkinter.Scrollbar(self,orient=Tkinter.HORIZONTAL)
                ascenseurHListePOS.grid(column=1,row=13,columnspan=4,sticky='NSEW')
                ascenseurHListePOS.configure(command=self.ListePOS.xview)
                self.ListePOS.configure(xscrollcommand=ascenseurHListePOS.set)

                self.ListePOS.bind('<Double-Button-1>',self.ListePOSdoubleclic)

                boutonSavePOS = Tkinter.Button(self, text=u"Sauver le corpus",command=self.FiltreurSavePOS)
                boutonSavePOS.grid(column=6,columnspan=1,row=11,sticky='SEW')
                boutonSaveNEG = Tkinter.Button(self, text=u"Sauver l'anticorpus",command=self.FiltreurSaveNEG)
                boutonSaveNEG.grid(column=6,columnspan=1,row=12,sticky='NEW')

                
                     
                        
        def sel_PRC(self):
                filepath = tkFileDialog.askopenfilename(filetypes=[("fichier de projet","*.prc")],title='Choisir le projet', initialdir='.')
                self.entry_PRC.delete(0,"end")
                self.entry_PRC.insert(0,filepath)
                PRC = open(filepath,'r').readlines()
                self.introPRC = PRC[:6]
                self.textesPRC = map(lambda x:re.sub('\n','',x),PRC[6:-1])
                self.LB1txt.set("%d texte(s) dans le projet" % (len(self.textesPRC)) )
                for i in self.textesPRC:
                        self.ListeNEG.insert("end",i)

        def  filtreurAdd(self):
                self.fenfiltreurAdd = Tkinter.Toplevel()
                self.fenfiltreurAdd.title(u"Filtreur : ajouter un élément au thème")
                self.filtreurAddEntry = Tkinter.Entry(self.fenfiltreurAdd,width=50)
                self.filtreurAddEntry.grid(column=1,row=1)
                filtreurAddButton = Tkinter.Button(self.fenfiltreurAdd,text=u"ajouter",command=self.filtreurAddAjoute)
                filtreurAddButton.grid(column=2,row=1)

        def  filtreurAddAjoute(self):
                item = self.filtreurAddEntry.get()
                theme = self.ListeDef.get(0,'end')
                if (not re.search('^\s*$',item) ):
                        if item not in theme:                 
                                self.ListeDef.insert("end",u"%s"%item)
                                self.fenfiltreurAdd.destroy()
                        else :
                                warning = Tkinter.Label(self.fenfiltreurAdd,text=u"%s est déjà dans le thème"%item,fg='red')
                                warning.grid(column=1,row=2)       

        def  filtreurRem(self):
                selec = self.ListeDef.curselection()
                if (selec):
                        self.ListeDef.delete(selec)
               

        def FiltreurEval(self):

                theme = self.ListeDef.get(0,'end')
                self.ListeTextesPos = []
                if len(self.textesPRC) > 0 and len(theme) > 0:
                        
                        SCORE = int(self.entry_Score.get())
                        DEP = int(self.entry_Dep.get())

                        self.ListeNEG.delete(0,"end")
                        self.ListePOS.delete(0,"end")

                        self.progress_bar()
                        progress = 0 

                                                
                        for t in self.textesPRC:
                                b = open(t,'r').read()
                                tests = []
                                testsResults = ""

                                for i in theme:
                                        AvAp = "[\s\.,;!\?\"']" #la liste des ponctuations et autres qui peuvent précéder ou suivre une forme
                                        index = "(^|(%s))(%s)((%s)|$)" % (AvAp,i,AvAp)
                                        index = re.compile(index)

                                        test = len(index.findall(b))
                                        if test > 0 :
                                                testsResults += "[%s:%d]" % (i,test)
                                        tests.append(test)

                                evaluation = [sum(tests),sum(1 for x in tests if x > 0)]
                                
                                
                                if (evaluation[0] >= SCORE) and (evaluation[1] >= DEP):
                                        self.ListePOS.insert("end","%s : score %d ; dep %d %s"%(t,evaluation[0],evaluation[1],testsResults))
                                        self.ListeTextesPos.append(t)
                                else :
                                        self.ListeNEG.insert("end","%s : score %d ; dep %d %s"%(t,evaluation[0],evaluation[1],testsResults))

                                progress += 1
                                self.progress_bar_avance(progress*100/len(self.textesPRC))
                                        
                        self.LB5txt.set("%d texte(s) valide(nt) la formule" % (len(self.ListeTextesPos)) )
                        self.LB1txt.set("%d texte(s) ne valide(nt) pas la formule" % len(set(self.textesPRC) - set(self.ListeTextesPos)))


        def ListeNEGdoubleclic(self,inutile):
                recup = self.ListeNEG.curselection()
                if (recup):
                        recup = self.ListeNEG.get(recup)
                        a_ouvrir = re.split(" :",recup)[0]
                        os.popen(a_ouvrir)

        def ListePOSdoubleclic(self,inutile):
                recup = self.ListePOS.curselection()
                if (recup):
                        recup = self.ListePOS.get(recup)
                        a_ouvrir = re.split(" :",recup)[0]
                        os.popen(a_ouvrir)

        def FiltreurSavePOS(self):
                if ( self.ListeTextesPos):
                        prcpos = list(self.introPRC) #essentiel pour éviter le phénomène de référence sur les listes
                        for t in self.ListeTextesPos:
                                prcpos.append(t+"\n")
                        prcpos.append("ENDFILE")
                        fichier = tkFileDialog.asksaveasfile(mode='w', filetypes=[("","*.prc")],defaultextension = ".prc",initialfile="")
                        fichier.writelines(prcpos)
                        fichier.close()

        def FiltreurSaveNEG(self):
                reste = list(set(self.textesPRC) - set(self.ListeTextesPos))
                if (reste):
                        prcneg = list(self.introPRC) #essentiel pour éviter le phénomène de référence sur les listes
                        for t in reste:
                                prcneg.append(t+"\n")
                        prcneg.append("ENDFILE")
                        fichier = tkFileDialog.asksaveasfile(mode='w', filetypes=[("","*.prc")],defaultextension = ".prc",initialfile="")
                        fichier.writelines(prcneg)
                        fichier.close()

        def filtreur_sav_config(self):
                theme = self.ListeDef.get(0,'end')
                if len(theme) > 0:
                        content = u""
                        for i in theme:
                                content += u"%s\n" % i
                fichier = tkFileDialog.asksaveasfile(mode='w', filetypes=[("","*.cfg")],defaultextension = ".cfg",initialfile="filtreur.cfg")
                fichier.write(content.encode('latin1'))
                fichier.close()

        def filtreur_recup_config(self,path):
                self.ListeDef.delete(0,"end") 
                for ligne in open(path,"r").readlines():
                        if not re.search("^\s*$",ligne):
                                self.ListeDef.insert("end",u"%s"%ligne[:-1].decode('latin1'))

        def filtreur_sel_conf(self):
                sel_conf = tkFileDialog.askopenfilename(title="sélectionner un fichier",filetypes=[("","*.cfg")],initialfile="filtreur.cfg",defaultextension = ".cfg")
                if (sel_conf):
                        self.filtreur_recup_config(sel_conf)

                
                
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 
## Menu base de données
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 

###############################################################
######## Factiva
###############################################################
                
        def factiva(self):
                for item in self.grid_slaves():
                        item.destroy()
                self.geometry("950x800")
                self.entry_rep = Tkinter.Entry(self,width=70)
                self.entry_rep.grid(column=2,row=1,sticky='NSEW')                
                bouton1 = Tkinter.Button(self, text=u"répertoire des fichiers sources", command= self.sel_dir)
                bouton1.grid(column=1,row=1,sticky='NSEW')
                boutonSupports = Tkinter.Button(self, text=u"sélectionner le support.publi", command= self.selecSupports)
                boutonSupports.grid(column=1,row=2,sticky='NSEW')
                self.entrySupports = Tkinter.Entry(self,width=70)
                self.entrySupports.grid(column=2,row=2,sticky='NSEW')
                bouton2 = Tkinter.Button(self, text=u"analyser les htm/html pour Factiva", command= self.lit_html)
                bouton2.grid(column=2,row=3,sticky='NSW')
                boutonDest = Tkinter.Button(self, text=u"répertoire de destination", command= self.sel_dirDest)
                boutonDest.grid(column=1,row=4,sticky='NSEW')
                self.entry_repDest = Tkinter.Entry(self,width=70)
                self.entry_repDest.grid(column=2,row=4,sticky='NSEW')
                self.ValCorrecCarateres= Tkinter.IntVar()
                correcCarateres = Tkinter.Checkbutton(self,text=u"nettoyer les caractères",variable = self.ValCorrecCarateres )
                correcCarateres.select()
                correcCarateres.grid(column=1,row=5,sticky='NSW')
                bouton3 = Tkinter.Button(self, text=u"traiter les htm/html pour Factiva", command= self.traiteFactiva)
                bouton3.grid(column=2,row=5,sticky='NSW')
                self.listebox = Tkinter.Listbox(self,height=20)
                self.listebox.grid(column=1,row=6,columnspan=2,sticky='NSEW')
                ascenseur1= Tkinter.Scrollbar(self)
                ascenseur1.grid(column=3,row=6,sticky='NSEW')
                ascenseur1.configure(command=self.listebox.yview)
                self.listebox.configure(yscrollcommand=ascenseur1.set)        
                self.afficheTexte = Tkinter.Text(self,height=20)
                self.afficheTexte.grid(column=1,row=7,columnspan=2,sticky='NSEW')
                ascenseur2= Tkinter.Scrollbar(self)
                ascenseur2.grid(column=3,row=7,sticky='NSEW')
                ascenseur2.configure(command=self.afficheTexte.yview)
                self.afficheTexte.configure(yscrollcommand=ascenseur2.set)
 

                cheminSupports = os.path.join( os.getcwd(), "support.publi")
                if os.path.isfile(cheminSupports) :
                        self.entrySupports.insert(0,cheminSupports)

        def sel_dirDest(self):
                self.entry_repDest.delete(0,"end")
                rep = tkFileDialog.askdirectory(title="sélectionner votre répertoire")
                self.entry_repDest.insert(0,rep)                   

        def selecSupports(self):
                filepath = tkFileDialog.askopenfilename(filetypes=[("fichier de supports","*.publi")],title='Choisir le fichier des supports', initialdir='.')
                self.entrySupports.delete(0,"end")
                self.entrySupports.insert(0,filepath)

        def liste_html(self,rep):
                liste_fichiers =  os.listdir(rep)
                liste_html = filter(lambda x : re.search("\.htm$|\.html$|\.HTML$",x), liste_fichiers)
                liste_html = map(lambda x : os.path.join(rep,x),liste_html)
                return liste_html
        
        def lit_html(self):
                self.listebox.delete(0,"end")
                rep = self.entry_rep.get()
                liste_html = self.liste_html(rep)
                supports = self.entrySupports.get()
                if (supports):
                        for item in sorted(liste_html):
                                prem = factiva.parsefactivahtm(item,supports)
                                self.listebox.insert("end","%s : %d article(s) ; %d support(s) inconnu(s), %d problème(s) de support" % (os.path.split(item)[1],prem.Narticles,len(prem.liste_inconnus),prem.pb_support ))
                                for inconnu in prem.liste_inconnus:
                                        self.afficheTexte.insert(1.0,"%s, support inconnu : %s\n" % (item,inconnu) )
                else :
                        self.afficheTexte.insert(1.0,"Il me manque le support.publi\n" )
            
        def traiteFactiva(self):
                cpt = 0
                rep = self.entry_rep.get()
                liste_html = self.liste_html(rep)
                for item in sorted(liste_html):
                        prem = factiva.parsefactivahtm(item,self.entrySupports.get())
                        if (prem.Narticles):
                                self.afficheTexte.insert(1.0,"Je traite %s\n" % (item) )
                                listeTXT = prem.traite(self.entry_repDest.get())
                                cpt +=  prem.fichiers_generes
                        if (self.ValCorrecCarateres.get()):
                                for TXT in listeTXT :
                                        le_fichier = text_cleaner.agit_dans_un_fichier(os.path.join(self.entry_repDest.get(),TXT))
                                        le_nettoyeur = text_cleaner.agent_de_surface(le_fichier.buf)
                                        le_fichier.corrige(le_nettoyeur.BUF)                           
                                
                self.afficheTexte.insert(1.0,"J'ai écrit %d fichier(s)\n"%cpt )

###############################################################
######## Europresse
###############################################################
                
        def europresse(self):
                for item in self.grid_slaves():
                        item.destroy()
                self.geometry("950x450")
                self.entry_rep = Tkinter.Entry(self,width=70)
                self.entry_rep.grid(column=2,row=1,sticky='NSEW')                
                bouton1 = Tkinter.Button(self, text=u"répertoire des fichiers sources", command= self.sel_dir)
                bouton1.grid(column=1,row=1,sticky='NSEW')
                boutonSupports = Tkinter.Button(self, text=u"sélectionner le support.publi", command= self.selecSupports)
                boutonSupports.grid(column=1,row=2,sticky='NSEW')
                self.entrySupports = Tkinter.Entry(self,width=70)
                self.entrySupports.grid(column=2,row=2,sticky='NSEW')
                boutonDest = Tkinter.Button(self, text=u"répertoire de destination", command= self.sel_dirDest)
                boutonDest.grid(column=1,row=3,sticky='NSEW')
                self.entry_repDest = Tkinter.Entry(self,width=70)
                self.entry_repDest.grid(column=2,row=3,sticky='NSEW')
                self.ValCorrecCarateres= Tkinter.IntVar()
                correcCarateres = Tkinter.Checkbutton(self,text=u"nettoyer les caractères",variable = self.ValCorrecCarateres )
                correcCarateres.select()
                correcCarateres.grid(column=1,row=4,sticky='NSW')
                bouton3 = Tkinter.Button(self, text=u"traiter les htm/html pour Europresse", command= self.traiteEuropresse)
                bouton3.grid(column=2,row=4,sticky='NSW')    
                self.afficheTexte = Tkinter.Text(self,height=20)
                self.afficheTexte.grid(column=1,row=5,columnspan=2,sticky='NSEW')
                ascenseur2= Tkinter.Scrollbar(self)
                ascenseur2.grid(column=3,row=5,sticky='NSEW')
                ascenseur2.configure(command=self.afficheTexte.yview)
                self.afficheTexte.configure(yscrollcommand=ascenseur2.set)

                cheminSupports = os.path.join( os.getcwd(), "support.publi")
                if os.path.isfile(cheminSupports) :
                        self.entrySupports.insert(0,cheminSupports)

        def sel_dirDest(self):
                self.entry_repDest.delete(0,"end")
                rep = tkFileDialog.askdirectory(title="sélectionner votre répertoire")
                self.entry_repDest.insert(0,rep)                   

        def selecSupports(self):
                filepath = tkFileDialog.askopenfilename(filetypes=[("fichier de supports","*.publi")],title='Choisir le fichier des supports', initialdir='.')
                self.entrySupports.delete(0,"end")
                self.entrySupports.insert(0,filepath)

        def traiteEuropresse(self):
                rep = self.entry_rep.get()
                liste_html = self.liste_html(rep)
                dest = self.entry_repDest.get()
                supports = self.entrySupports.get()
                if (supports):
                        for item in liste_html:
                                traite = Europresse_HTML.parseEuropressHTML(item,supports,dest)
                                listeTXT = traite.listeFichiersecrits
                                self.afficheTexte.insert(1.0,"J'ai créé %d fichier(s)\n" % len(listeTXT))
                                if (self.ValCorrecCarateres.get()):
                                        for TXT in listeTXT :
                                                le_fichier = text_cleaner.agit_dans_un_fichier(os.path.join(self.entry_repDest.get(),TXT))
                                                le_nettoyeur = text_cleaner.agent_de_surface(le_fichier.buf)
                                                le_fichier.corrige(le_nettoyeur.BUF)
                else :
                        self.afficheTexte.insert(1.0,"Il me manque le support.publi\n" )
                        
                

###############################################################
######## Lexis Nexis
###############################################################
                
        def lexis(self):
                for item in self.grid_slaves():
                        item.destroy()
                self.geometry("850x450")
                self.entry_rep = Tkinter.Entry(self,width=70)
                self.entry_rep.grid(column=2,row=1,sticky='NSEW')                
                bouton1 = Tkinter.Button(self, text=u"répertoire des fichiers sources", command= self.sel_dir)
                bouton1.grid(column=1,row=1,sticky='NSEW')
                boutonSupports = Tkinter.Button(self, text=u"sélectionner le support.publi", command= self.selecSupports)
                boutonSupports.grid(column=1,row=2,sticky='NSEW')
                self.entrySupports = Tkinter.Entry(self,width=70)
                self.entrySupports.grid(column=2,row=2,sticky='NSEW')
                boutonDest = Tkinter.Button(self, text=u"répertoire de destination", command= self.sel_dirDest)
                boutonDest.grid(column=1,row=3,sticky='NSEW')
                self.entry_repDest = Tkinter.Entry(self,width=70)
                self.entry_repDest.grid(column=2,row=3,sticky='NSEW')
                self.ValCorrecCarateres= Tkinter.IntVar()
                correcCarateres = Tkinter.Checkbutton(self,text=u"nettoyer les caractères",variable = self.ValCorrecCarateres )
                correcCarateres.select()
                correcCarateres.grid(column=1,row=4,sticky='NSW')
                bouton3 = Tkinter.Button(self, text=u"traiter les .txt/.TXT pour Lexis Nexis", command= self.traiteLexis)
                bouton3.grid(column=2,row=4,sticky='NSW')    
                self.afficheTexte = Tkinter.Text(self,height=20)
                self.afficheTexte.grid(column=1,row=5,columnspan=2,sticky='NSEW')
                ascenseur2= Tkinter.Scrollbar(self)
                ascenseur2.grid(column=3,row=5,sticky='NSEW')
                ascenseur2.configure(command=self.afficheTexte.yview)
                self.afficheTexte.configure(yscrollcommand=ascenseur2.set)

                cheminSupports = os.path.join( os.getcwd(), "support.publi")
                if os.path.isfile(cheminSupports) :
                        self.entrySupports.insert(0,cheminSupports)

        def sel_dirDest(self):
                self.entry_repDest.delete(0,"end")
                rep = tkFileDialog.askdirectory(title="sélectionner votre répertoire")
                self.entry_repDest.insert(0,rep)                   

        def selecSupports(self):
                filepath = tkFileDialog.askopenfilename(filetypes=[("fichier de supports","*.publi")],title='Choisir le fichier des supports', initialdir='.')
                self.entrySupports.delete(0,"end")
                self.entrySupports.insert(0,filepath)

        def traiteLexis(self):
                rep = self.entry_rep.get()
                liste_fichiers =  os.listdir(rep)
                liste_txt = filter(lambda x : re.search("\.txt$|\.TXT$",x), liste_fichiers)
                liste_txt = map(lambda x : os.path.join(rep,x),liste_txt)
                dest = self.entry_repDest.get()
                supports = self.entrySupports.get()
                if (supports):
                        for item in liste_txt:
                                self.afficheTexte.insert(1.0,"Je traite %s \n" %  item )
                                traite = lexis.parseLEXISNEXIS(item,supports,dest)
                                listeTXT = traite.listeFichiersecrits
                                self.afficheTexte.insert(1.0,"J'ai créé %d fichier(s)\n" % len(listeTXT))
                                if (self.ValCorrecCarateres.get()):
                                        for TXT in listeTXT :
                                                le_fichier = text_cleaner.agit_dans_un_fichier(os.path.join(self.entry_repDest.get(),TXT))
                                                le_nettoyeur = text_cleaner.agent_de_surface(le_fichier.buf)
                                                le_fichier.corrige(le_nettoyeur.BUF)
                                if (len(traite.supportsInconnus)) :
                                        self.afficheTexte.insert(1.0,"J'ai trouvé %d support(s) inconnu(s)\n" % (len(traite.supportsInconnus)))

                                                
                else :
                        self.afficheTexte.insert(1.0,"Il me manque le support.publi\n" )

      

###############################################################
######## QP
###############################################################
        def questionsParlementaires(self):
                for item in self.grid_slaves():
                        item.destroy()
                self.geometry("900x900")
                LB1F1 = Tkinter.Label(self,text="mots clefs")
                LB1F1.grid(row=1,column=3,sticky='NSW')
                self.entr_F11 = Tkinter.Entry(self)
                self.entr_F11.grid(row=1,column=1,columnspan=2,sticky='NSEW')
                
                F12 = Tkinter.Label(self,text="Sénat : intervalle temporel", fg="blue")
                F12.grid(row=2,column=1,columnspan=2,sticky='NSW')
                F12a = Tkinter.Label(self,text="début")
                F12a.grid(row=3,column=1,sticky='NSEW')
                self.entr_F121 = Tkinter.Entry(self)
                self.entr_F121.grid(row=4,column=1,sticky='NSEW')
                self.entr_F121.insert(0,time.strftime("%d/%m/" ) + str( int(time.strftime("%Y" )) - 3))
                F12b = Tkinter.Label(self,text="fin")
                F12b.grid(row=5,column=1,sticky='NSEW')
                self.entr_F122 = Tkinter.Entry(self)
                self.entr_F122.grid(row=6,column=1,sticky='NSEW')
                self.entr_F122.insert(0,time.strftime("%d/%m/%Y" ))
                
                self.F13 = Tkinter.Label(self,text="Assemblée : législatures", fg="blue")
                self.F13.grid(row=2,column=2,sticky='NSEW')
                self.LF13 = Tkinter.Listbox(self, height=9, width=30, selectmode=Tkinter.MULTIPLE)
                for leg in ["7e (02/07/1981-01/04/1986)",
                            "8e (02/04/1986-14/05/1988)",
                            "9e (23/06/1988-01/04/1993)",
                            "10e (02/04/1993-21/04/1997)",
                            "11e (01/06/1997-18/06/2002) ",
                            "12e (19/06/2002-19/06/2007)",
                            "13e (20/06/2007-19/06/2012)",
                            "14e (20/06/2012-20/06/2017)",
                            "15e (20/06/2017-)"
                            ]:
                        self.LF13.insert(Tkinter.END,leg)
                self.LF13.selection_set(first=8)
                self.LF13.grid(row=3,column=2,rowspan=4)                
                
                bou2F1 = Tkinter.Button(self, text='rechercher',command=self.chercheQP)
                bou2F1.grid(row=6,column=3,sticky='NSW')

                self.listeboxQP=Tkinter.Listbox(self,height=20,width=110,selectmode=Tkinter.EXTENDED)
                self.listeboxQP.grid(row=7,column=1,columnspan=3,sticky='NSEW')
                ascenseur1= Tkinter.Scrollbar(self)
                ascenseur1.grid(column=4,row=7,sticky='NSEW')
                ascenseur1.configure(command=self.listeboxQP.yview)
                self.listeboxQP.configure(yscrollcommand=ascenseur1.set)
                self.listeboxQP.bind('<Double-Button-1>',self.QPdoubleclic)
                
                bou3 = Tkinter.Button(self, text="tout sélectionner",command=self.QPselect_all)
                bou3.grid(row=8,column=1,sticky='NSW')
                self.ValCorrecCarateres= Tkinter.IntVar()
                correcCarateres = Tkinter.Checkbutton(self,text=u"nettoyer les caractères",variable = self.ValCorrecCarateres )
                correcCarateres.select()
                correcCarateres.grid(column=2,row=8,sticky='NSW')
                bou4=Tkinter.Button(self, text="traiter la sélection",command=self.QPtraite)
                bou4.grid(row=8,column=3,sticky='NSW')

                LB1F2 = Tkinter.Button(self, text="Chemin du répertoire final pour les CTX",command=self.QPchoisir_rep)
                LB1F2.grid(row=9,column=1,sticky='NSE')
                self.entr_F2 = Tkinter.Entry(self)
                self.entr_F2.grid(row=9,column=2,columnspan=2,sticky='NSEW')
                LB1F3 = Tkinter.Button(self, text="Répertoire d'écriture des fichier",command=self.QPchoisir_repTXT)
                LB1F3.grid(row=10,column=1,sticky='NSE')
                self.entr_F3 = Tkinter.Entry(self)
                self.entr_F3.grid(row=10,column=2,columnspan=2,sticky='NSEW')
                
                self.afficheTexte = Tkinter.Text(self,height=5)
                self.afficheTexte.grid(column=1,row=12,columnspan=3,sticky='NSEW')
                ascenseur2= Tkinter.Scrollbar(self)
                ascenseur2.grid(column=4,row=12,sticky='NSEW')
                ascenseur2.configure(command=self.afficheTexte.yview)
                self.afficheTexte.configure(yscrollcommand=ascenseur2.set)
                
                
        def QPselect_all(self):
                self.listeboxQP.selection_set(0,Tkinter.END)

        def QPdoubleclic(self,inutile):
                L=self.listeboxQP.curselection()
                if (len(L) == 1) :
                        question = self.QPlisteLiensT[int(L[0])]
                        if ((question != "SENAT") and (question != "ASSEMBLEE")):
                                if (re.search("http://questions.assemblee-nationale.fr",question)):
                                        url = question
                                else:
                                        url = "http://www.senat.fr/basile/visio.do?id=%s" % question
                                webbrowser.open(url,0,1)                

        def chercheQP(self):
                self.listeboxQP.delete(0,"end")
                de = self.entr_F121.get()
                au = self.entr_F122.get()
                leg = self.LF13.curselection()
                mot_clefs = self.entr_F11.get().encode('latin-1')
                if (mot_clefs):
                        self.afficheTexte.insert(1.0,"Je cherche [%s] dans les bases parlementaires, cela peut prendre du temps\n" % mot_clefs)
                        self.update()
                        try:
                                ASS,assembleeLiens,SENAT,senatLiens = qp.recherche(mot_clefs,de,au,leg)
                                ASS.reverse()
                                assembleeLiens.reverse()
                                self.QPlisteLiensT = ["SENAT"] + senatLiens + ["ASSEMBLEE"] + assembleeLiens
                                listeQP = []
                                self.listeboxQP.insert(Tkinter.END, "SENAT : %d question(s)" % len(SENAT))
                                for element in SENAT:
                                        self.listeboxQP.insert(Tkinter.END, element)
                                listeQP.extend(SENAT)
                                self.listeboxQP.insert(Tkinter.END, "ASSEMBLEE: %d question(s)" % len(ASS))
                                for element in ASS:
                                        self.listeboxQP.insert(Tkinter.END, element)
                                listeQP.extend(ASS)
                        except:
                                self.afficheTexte.insert(1.0,"Probleme de connexion, réessayer plus tard\n" )
                                
                        
        def QPchoisir_rep(self):
                self.entr_F2.delete(0,Tkinter.END)
                R = tkFileDialog.askdirectory(title='Sélectionner le répertoire cible')
                self.entr_F2.insert(Tkinter.END,R)
                
        def QPchoisir_repTXT(self):
                self.entr_F3.delete(0,Tkinter.END)
                R = tkFileDialog.askdirectory(title='Sélectionner le répertoire cible')
                self.entr_F3.insert(Tkinter.END,R)  

        def QPtraite(self):
                selec =  self.listeboxQP.curselection()
                if (selec):
                        ##on récupère le répertoire cible
                        final = self.entr_F2.get()
                        cible = self.entr_F3.get()
                        if (cible == "") :
                                cible = os.getcwd()
                        self.progress_bar()
                        progress = 0         
                        for question in selec:
                                lien = self.QPlisteLiensT[int(question)]
                                if ((lien != "SENAT") and (lien != "ASSEMBLEE")):
                                        #self.afficheTexte.insert(1.0,u"Je traite la question %s\n"%self.listeboxQP.get(question) )
                                        self.update()
                                        try :
                                                listeFichiers = qp.traite(lien,cible,final)
                                                #self.afficheTexte.insert(1.0,u"J'ai généré %d fichiers : %s\n" % ( len(listeFichiers), ", ".join(listeFichiers) ) )
                                        except:
                                                self.afficheTexte.insert(1.0,u"J'ai eu un probleme avec la question %s\n" % lien)
                                                listeFichiers = []
                                        self.update()
                                        if (self.ValCorrecCarateres.get()):
                                                for TXT in  map(lambda x : os.path.join(cible,x), listeFichiers):
                                                        if (os.path.splitext(TXT)[1] == '.txt') :
                                                                le_fichier = text_cleaner.agit_dans_un_fichier(TXT)
                                                                le_nettoyeur = text_cleaner.agent_de_surface(le_fichier.buf)
                                                                le_fichier.corrige(le_nettoyeur.BUF)
                                progress += 1
                                self.progress_bar_avance(progress*100/len(selec))
                                        

###############################################################
##appli qui permet de télécharger le support.publi
###############################################################
        def recup_support(self):
                R = tkFileDialog.askdirectory(title='Sélectionner le répertoire de sauvegarde du fichier')
                if (R):
                        try :
                                urllib.urlretrieve("http://prosperologie.org/outils/export_support.php",os.path.join(R,"support.publi"))
                        except :
                                alert=Tkinter.Toplevel(self)
                                texte =Tkinter.Message(alert,bg="white",text="Erreur lors du téléchargement du support.publi, vérifiez votre connexion ou les droits d'écriture du dossier")
                                texte.pack()
                                ferme=Tkinter.Button(alert,text="Fermer",command=alert.destroy)
                                ferme.pack()

                
        

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 
## Menu Traitements
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 


###############################################################
##appli qui permet de faire un tableau des années citées récupérées
###############################################################
        def annees_citees(self):
                for item in self.grid_slaves():
                        item.destroy()
                self.geometry("950x850")

                texte1 = Tkinter.Label(text=u"Récupéré par les formules")
                texte1.grid(column=2,row=1)
                
                BoutonG0 = Tkinter.Button(self,text=u"coller", command=self.AC_colle)
                BoutonG0.grid(column=1,row=2,sticky='NEW')       
                BoutonG1 = Tkinter.Button(self,text=u"calculer", command=self.AC_calcule)
                BoutonG1.grid(column=1,row=3,sticky='NEW')
                BoutonG2 = Tkinter.Button(self,text=u"effacer", command=self.AC_effaceZT1)
                BoutonG2.grid(column=1,row=4,sticky='NEW')
        
                self.AC_ZONEtexte1 = Tkinter.Text(self,width=30,height=50)
                self.AC_ZONEtexte1.grid(column=2,row=2,rowspan=4,sticky='NSEW')        
                ascenseur1= Tkinter.Scrollbar(self)
                ascenseur1.grid(column=3,row=2,rowspan=4,sticky='NSEW')
                ascenseur1.configure(command=self.AC_ZONEtexte1.yview)
                self.AC_ZONEtexte1.configure(yscrollcommand=ascenseur1.set)

                texte2 = Tkinter.Label(text=u"Calcul")
                texte2.grid(column=4,row=1)

                BoutonD0 = Tkinter.Button(self,text=u"copier", command=self.AC_copier)
                BoutonD0.grid(column=6,row=2,sticky='NEW')
                BoutonD2 = Tkinter.Button(self,text=u"effacer", command=self.AC_effaceZT2)
                BoutonD2.grid(column=6,row=3,sticky='NEW')
                BoutonD2 = Tkinter.Button(self,text=u"sauvegarder", command=self.AC_sauve)
                BoutonD2.grid(column=6,row=4,sticky='NEW')
                
                self.AC_ZONEtexte2 = Tkinter.Text(self,width=30,height=50)
                self.AC_ZONEtexte2.grid(column=4,row=2,rowspan=4,sticky='NSEW')
                ascenseur2= Tkinter.Scrollbar(self)
                ascenseur2.grid(column=5,row=2,rowspan=4,sticky='NSEW')
                ascenseur2.configure(command=self.AC_ZONEtexte2.yview)
                self.AC_ZONEtexte2.configure(yscrollcommand=ascenseur2.set)       

        def AC_effaceZT1(self):
                self.AC_ZONEtexte1.delete(1.0,"end")
                self.AC_ZONEtexte1.update()        

        def AC_effaceZT2(self):
                self.AC_ZONEtexte2.delete(1.0,"end")
                self.AC_ZONEtexte2.update()

        def AC_calcule(self):
                BUF =  self.AC_ZONEtexte1.get(1.0,"end")

                mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre",
                "JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOUT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE",
                "fevrier", "FEVRIER", "aout", "AOUT", "decembre", "Decembre"]

                annees = []
                for a in re.findall(' (\d{4}\t\d*)',BUF):
                    annees.append(a)
                for m in mois:
                    for a in re.findall("%s (\d{2}\t\d*)"% m,BUF):
                        if (a[0] == "0") :
                            annees.append("20%s" %a)
                        else :
                            annees.append("19%s" %a)

                anneesSomme = {}
                while (annees):
                    A = re.split('\t',annees.pop())
                    if anneesSomme.has_key(int(A[0])):
                        anneesSomme[int(A[0])] += int(A[1])
                    else :
                        anneesSomme[int(A[0])] = int(A[1])

                anneesFiltre = {}
                for A in anneesSomme.keys():
                    if  (anneesSomme[A] > 0):#la valeur minimale
                        anneesFiltre[A] = anneesSomme[A]

                self.AC_ZONEtexte2.delete(1.0,"end")
                self.AC_ZONEtexte2.update()
                for A in range(sorted(anneesFiltre.keys())[0],sorted(anneesFiltre.keys())[-1]+1,1):
                    if anneesFiltre.has_key(A):
                        self.AC_ZONEtexte2.insert("end","%s\t%s\n" % (A,anneesFiltre[A]))
                    else:
                        self.AC_ZONEtexte2.insert("end","%s\t0\n" % (A))

        def AC_colle(self):
                self.AC_ZONEtexte1.delete(1.0,"end")
                self.AC_ZONEtexte1.insert("end",self.AC_ZONEtexte1.clipboard_get())

        def AC_copier(self):
                BUF =  self.AC_ZONEtexte2.get(1.0,"end")
                self.AC_ZONEtexte2.clipboard_clear()
                self.AC_ZONEtexte2.clipboard_append(BUF)
                
        def AC_sauve(self):
                BUF =  self.AC_ZONEtexte2.get(1.0,"end")
                BUF = re.sub("\t",";",BUF)
                fichier = tkFileDialog.asksaveasfile(mode='w', filetypes=[("Comma-separated values","*.csv")],defaultextension = ".csv",initialfile="annees_citees.csv")
                if ( fichier ):
                        fichier.write(BUF)
                        fichier.close()

###############################################################
##appli pour générer des cartes à partir des qp
###############################################################
        def carteqp(self):
                for item in self.grid_slaves():
                        item.destroy()
                self.geometry("280x450")
                texte1 = Tkinter.Label(text=u"Copier la liste département -> valeur")
                texte1.grid(column=1,columnspan=3,row=1)
                self.carteqp_ZONEtexte1 = Tkinter.Text(self,width=30,height=25)
                self.carteqp_ZONEtexte1.grid(column=1,columnspan=3,row=2,sticky='NSEW')        
                ascenseur1= Tkinter.Scrollbar(self)
                ascenseur1.grid(column=4,row=2,sticky='NSEW')
                ascenseur1.configure(command=self.carteqp_ZONEtexte1.yview)
                self.carteqp_ZONEtexte1.configure(yscrollcommand=ascenseur1.set)
                Bouton1 = Tkinter.Button(self,text=u"coller", command=self.carteqp_colle)
                Bouton1.grid(column=1,row=4,sticky='NEW')
                Bouton2 = Tkinter.Button(self,text=u"effacer", command=self.carteqp_efface)
                Bouton2.grid(column=2,row=4,sticky='NEW')  
                Bouton3 = Tkinter.Button(self,text=u"traiter", command=self.carteqp_traite)
                Bouton3.grid(column=3,row=4,sticky='NEW')

        def carteqp_colle(self):
                self.carteqp_ZONEtexte1.delete(1.0,"end")
                self.carteqp_ZONEtexte1.insert("end",self.carteqp_ZONEtexte1.clipboard_get())

        def carteqp_efface(self):
                self.carteqp_ZONEtexte1.delete(1.0,"end")
                

        def carteqp_traite(self):
                donnees = self.carteqp_ZONEtexte1.get(1.0,"end")
                if (donnees != "\n"): 
                        fichier = tkFileDialog.asksaveasfilename(title="Enregistrer sous", initialdir=".", initialfile="carte.svg", filetypes = [("Fichiers svg","*.svg;")])
                        carteqp.traite(donnees,fichier)
                        webbrowser.open(fichier,0,1)
                        

                            


if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.mainloop()



