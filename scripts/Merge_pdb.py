import os
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir('./Type_1/sampling') if isfile(join('./Type_1/sampling/', f))]
onlyfiles = onlyfiles[1:]
print(onlyfiles)

#os.mkdir('./Type_1/pdb_merge')


recepteur = input('Entrez le nom du fichier à analyser : ')
while recepteur == '':
	print('Merci de renseigner un nom de fichier pour l\'execution du programme')
	recepteur = input('Entrez le nom du fichier à analyser : ')

if os.path.exists(recepteur):
	print("le fichier est présent")
else:
	print('Le fichier que vous avez rentré n\'est pas sur votre disque dur')
	recepteur = input('Entrez le nom du fichier à analyser : ')


for fichier in onlyfiles:
	with open('./Type_1/pdb_merge/{}_merge.pdb'.format(fichier), 'w') as filout:
		with open('./Type_1/structures-natives/{}'.format(recepteur), 'r') as recep:
			for ligne in recep:
				if ligne[0:6].strip() == 'ATOM':
					ligne = ligne[:21] + 'A' + ligne[22:]
					filout.write(ligne)
		filout.write('TER \n')
		with open('./Type_1/sampling/{}'.format(fichier), 'r') as ligand:
			for ligne in ligand:
				if ligne[0:6].strip() == 'ATOM':
					ligne = ligne[:21] + 'B' + ligne[22:]
					filout.write(ligne)
			
			
						