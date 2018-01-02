#!/usr/bin/env python3

import sys
import os
import numpy as np

def recup_results(fichier):
    """ Fonction qui récupère les données des valeurs contenues dans le fichier
    resultats.out
    Input : fichier de résultats
    Outputs : recup_results(fichier)[0] = statpot
              recup_results(fichier)[1] = wdv
              recup_results(fichier)[2] = electro
              recup_results(fichier)[3] = shape
              recup_results(fichier)[4] = TMscore
    """
    #On récupère le statpot
    liste = []
    statpot = []
    command = "awk -F'\t' '{print $4}'"
    os.system( "{} {} > statpot.out".format(command, fichier))
    with open('statpot.out' , 'r') as filin:
	    for ligne in filin:
		    liste.append(ligne[:-1])
    for nombre in liste[2:]:
        statpot.append(float(nombre))
    os.system('rm statpot.out')

    #On récupère le wdv
    wdv = []
    liste = []
    command = "awk -F'\t' '{print $5}'"
    os.system("{} {} > wdv.out".format(command, fichier))
    with open('wdv.out' , 'r') as filin:
	    for ligne in filin:
		    liste.append(ligne[:-1])
    for nombre in liste[2:]:
        wdv.append(float(nombre))
    os.system('rm wdv.out')

    #On récupère le electro
    electro = []
    liste = []
    command = "awk -F'\t' '{print $6}'"
    os.system("{} {} > electro.out".format(command, fichier))
    with open('electro.out' , 'r') as filin:
	    for ligne in filin:
		    liste.append(ligne[:-1])
    for nombre in liste[2:]:
        electro.append(float(nombre))
    os.system('rm electro.out')

    #On récupère le shape
    shape = []
    liste = []
    command = "awk -F'\t' '{print $7}'"
    os.system("{} {} > shape.out".format(command, fichier))
    with open('shape.out' , 'r') as filin:
	    for ligne in filin:
		    liste.append(ligne[:-1])
    for nombre in liste[2:]:
        shape.append(float(nombre))
    os.system('rm shape.out')

    #On récupère le TMscore
    TMscore = []
    liste = []
    command = "awk -F'\t' '{print $10}'"
    os.system("{} {} > TM.out".format(command, fichier))
    with open('TM.out' , 'r') as filin:
	    for ligne in filin:
		    liste.append(ligne[:-1])
    for nombre in liste[2:]:
        TMscore.append(float(nombre))
    os.system('rm TM.out')
    
    return statpot, wdv, electro, shape, TMscore

def normalize(liste):
    """Fonction qui normalise les données numériques d'une liste
    Input : liste de données numériques
    Output : liste des donnnées normalisées entre 0 et 1
    """
    liste_norm = []
    mini = min(liste)
    maxi = max(liste)
    for nombre in liste:
        normalise = (float(nombre) - mini)/(maxi-mini)
        liste_norm.append(float(normalise))
    
    return liste_norm
   
    
################################################
####Programme principal#########################
################################################

norm_statpot = normalize(recup_results('./meet-U/lib/resultats.out')[0])
norm_wdv = normalize(recup_results('./meet-U/lib/resultats.out')[1])
norm_electro = normalize(recup_results('./meet-U/lib/resultats.out')[2])
norm_shape = normalize(recup_results('./meet-U/lib/resultats.out')[3])
norm_TMscore = normalize(recup_results('./meet-U/lib/resultats.out')[4])


matrice = [norm_statpot , norm_wdv , norm_electro , norm_shape]
print(np.array(matrice))
