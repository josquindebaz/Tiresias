# -*- encoding: iso-8859-1 -*-
import re
import os

class ProsperoFile(object):
    """Write Prospero Files
    input : dd/mm/yyyy + prefix
    output files .tx and .ctx without duplicate in the directory"""

    def __init__(self, date, prefix, dest="."):
        #instancie l'objet avec une date et une racine, lui donne son nom
        if (not os.path.isdir(dest)):
                os.mkdir(dest)
        self.nom_fichier = self.nom_fichier_sans_doublon(date, prefix.strip(), dest)

    def date_prosperienne(self,date):
        #la date de depart doit avoir la forme jj/mm/aaaa
        mois = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C")   #les mois en tuple
        date = re.split('/', date)
        date = "%s%s%s" % (date[2][2:], mois[int(date[1])-1], date[0])
        return date

    def nom_fichier_sans_doublon(self, date, racine, dest):
        indice,base = "A", 64
        nom = "%s/%s%s%s" % (dest, racine, self.date_prosperienne(date), indice)
        while os.path.isfile(nom + ".txt"): #tant que le fichier existe
            if  (ord(indice[-1]) < 90):
                indice = chr(ord(indice[-1]) + 1) #incrémente le dernier caractère de l'indice
            else :		#quand on arrive à Z
                base += 1	#augmente la première lettre
                indice = "A"	#remet la deuxième à A
            if base > 64 : #à deux lettres
                indice = chr(base) + indice
            nom = "%s/%s%s%s" % (dest, racine, self.date_prosperienne(date), indice)
        return nom

    def fin_de_ligne (self, lignes):
        lignes += "\n"
        return lignes

    def ecrit(self, contenu_fichier, extention):	#écrit le fichier,  selon une liste de contenu et une extension
        nom_fichier = self.nom_fichier + extention	#ajoute l'extention
        pointeur_fichier = open(nom_fichier, 'w')
        texte_fichier = map(self.fin_de_ligne, contenu_fichier) 	#ajoute les fins de ligne
        pointeur_fichier.writelines(texte_fichier)	#écrit les lignes du fichier
        pointeur_fichier.close()
        return nom_fichier


