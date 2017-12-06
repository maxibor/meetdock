#!/usr/bin/env python3

import os
import sys
import re

lib_path = os.getcwd()

def parser_tmscore(fichier):

	""" """
	dico_valeurs = {}
	
	with open(fichier, 'r') as filin:
		#définition des expressions régulières afin de rechercher dans le résultat
		#les valeurs du TMscore, du RMSD et du RMSD_align
		regex_TMscore = re.compile('TM-score.*=.*([0-9]+\.[0-9]+) .*')
		regex_RMSD = re.compile('RMSD.*=.*([0-9][0-9]\.[0-9]+)')
		regex_RMSD_aling = re.compile('Super.*RMSD=*.*([0-9]+\.[0-9]+)')

		#Parcours de toutes les lignes du resultat du score rendu par le programme
		#TMscore
		for ligne in filin:
			#Recherche des expressions régulières dans le fichier résultat
			TMscore = regex_TMscore.search(ligne)
			RMSD = regex_RMSD.search(ligne)
			RMSD_align = regex_RMSD_aling.search(ligne)

			#Si les résultats sont trouvés alors on les print
			if TMscore != None:
				dco_valeurs[str(fichier.split('/')[-1])] = TMscore.group(1)
			elif RMSD != None:
				dco_valeurs[str(fichier.split('/')[-1])] = RMSD.group(1)
			elif RMSD_align != None:
				dco_valeurs[str(fichier.split('/')[-1])] = RMSD_align.group(1)

    return dico_valeurs
# {'tmscore':valeur, 'rmsd avant alignement': valeur, 'rmsd apres alignement' : valeur }

def zang_scores_calculs(pdbpath, nativepath):
        
    output = str(lib_path)+'/../temp/'+str(pdbpath.split('/')[-1])+'_tmscore.out'
    command = ('TMscore {} {} > '+str(output)).format(pdbpath,nativepath)
    os.system(command)

    resultat = parser_tmscore(str(output))
    
    return resultat


############################
###Programme principal#####
############################

if __name__ == '__main__':
    zang_scores_calculs('./pdbtest.pdb', './natiftest.pdb')
