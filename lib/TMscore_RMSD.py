#!/usr/bin/env python3


import os
import sys
import re

lib_path = os.getcwd()

def parser_tmscore(fichier):
	''' Function which parse the TMscore file and look for three different scores, 
	TMscore, RMSD, RMSD post alignment.
	Input : TMscore_result file
	Output : Dictionnary which contain three keys 'tmscore', 'rmsd', 'rmsd_alig'. 
	Each value is the specific score obtained.
	'''

    dico_valeurs = {}
	
    with open(fichier, 'r') as filin:
        #définition des expressions régulières afin de rechercher dans le résultat
        #les valeurs du TMscore, du RMSD et du RMSD_align
        regex_TMscore = re.compile('TM-score.*=.*([0-9]+\.[0-9]+) .*')
        regex_RMSD = re.compile('RMSD.*=.*([0-9]+\.[0-9]+)')
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
                dico_valeurs['tmscore'] = TMscore.group(1)
            if RMSD != None:
                dico_valeurs['rmsd'] = RMSD.group(1)
            if RMSD_align != None:
                #print(RMSD_align.group(1))
                dico_valeurs['rmsd_align'] = RMSD_align.group(1)
       
        
    return dico_valeurs
# {'tmscore':valeur, 'rmsd avant alignement': valeur, 'rmsd apres alignement' : valeur }

def zang_scores_calculs(pdbpath, nativepath):
	'''Function which use the executable TMscore form https://zhanglab.ccmb.med.umich.edu/
	Input : path of the native complex and path of the model that you want to evalue
	Output : TMscore_result file'''
        
    output = str(lib_path)+'/../temp/'+str(pdbpath.split('/')[-1])+'_tmscore.out'
    command = ('TMscore -c {} {} > '.format(pdbpath, nativepath)+str(output))
    os.system(command)

    resultat = parser_tmscore(str(output))
    
    return resultat


############################
###Programme principal#####
############################

if __name__ == '__main__':
    #zang_scores_calculs('./pdbtest.pdb', './natiftest.pdb')
    print(parser_tmscore('./tmout'))
