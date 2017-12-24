import os

os.chdir('./chaines_correctes')
liste_pdb = os.listdir()

new_ligne = ''

for chaque_pdb in liste_pdb:
    fichier_pdb = open(chaque_pdb, 'r')

    #then
    for ligne in fichier_pdb:
        print('ATOM = \''+str(ligne[0:6]+'\''))
        print('atom serial number = \''+str(ligne[6:11])+'\'')
        print('atom_name = \''+str(ligne[12:16]+'\''))
        print('alternate location indicator = \''+str(ligne[16:17]+'\''))
        print('residue name = \''+str(ligne[17:20]+'\''))
        print('chain identifier = \''+str(ligne[21:22]+'\''))
        print('residue sequence number = \''+str(ligne[22:26]+'\''))
        print('code for insertion of residues = \''+str(ligne[26:27]+'\''))
        print('orthogonal X = \''+str(ligne[30:38]+'\''))
        print('orthogonal Y = \''+str(ligne[38:46]+'\''))
        print('orthogonal Z = \''+str(ligne[46:54]+'\''))
        print('occupancy = \''+str(ligne[54:60]+'\''))
        print('temperature factor = \''+str(ligne[60:66]+'\''))

        
    fichier_pdb.close()
        
