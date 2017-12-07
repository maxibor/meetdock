import os
from os import listdir
from os.path import isfile, join

def merge_pdb(receptor_path, ligand_path, outputpath='./merged_pdb'):
	'''
	 Take two pdb as input and merge them into a third one using the specified
	 PATH. In no path is specified, it is written in current working directory
	 under "merged.pdb"
	 Input : two pdb, a receptor and a ligand for example
	 Output : Third pdb file which is the association of the two outputs.
	 IMPORTANT : all chains are renamed !!!! Chain A for the first input pdb file
	 and Chain B for the second pdb file
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
