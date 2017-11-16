#GRAVEY Francois

#Commentaire de Guillaume: J'ai modifié ton code pour qu'il rentre dans une
#..fonction
#Il faudrait écrire un test et vérifier que ça marche :)

import os
from os import listdir
from os.path import isfile, join


# onlyfiles = [f for f in listdir('./Type_1/sampling') if isfile(join('./Type_1/sampling/', f))]
# onlyfiles = onlyfiles[1:]
# print(onlyfiles)
#
# #os.mkdir('./Type_1/pdb_merge')
#
#
# recepteur = input('Entrez le nom du fichier à analyser : ')
# while recepteur == '':
# 	print('Merci de renseigner un nom de fichier pour l\'execution du programme')
# 	recepteur = input('Entrez le nom du fichier à analyser : ')
#
# if os.path.exists(recepteur):
# 	print("le fichier est présent")
# else:
# 	print('Le fichier que vous avez rentré n\'est pas sur votre disque dur')
# 	recepteur = input('Entrez le nom du fichier à analyser : ')

def merge_pdb(receptor_path, ligand_path, outputpath='./merged_pdb'):
	'''
	 Take two pdb as input and merge them into a third one using the specified
	 PATH. In no path is specified, it is written in current working directory
	 under "merged.pdb"
	'''

	# for fichier in onlyfiles: #Not needed if we're working on a single pdb
	try:
		with open(outputpath, 'w') as filout:
			with open(receptor_path, 'r') as recep:
				for ligne in recep:
					if ligne[0:6].strip() == 'ATOM':
						ligne = ligne[:21] + 'A' + ligne[22:]
						filout.write(ligne)
			filout.write('TER \n')
			with open(ligand_path, 'r') as ligand:
				for ligne in ligand:
					if ligne[0:6].strip() == 'ATOM':
						ligne = ligne[:21] + 'B' + ligne[22:]
						filout.write(ligne)

if __name__ == '__main__':
	#Tests needs to be written
