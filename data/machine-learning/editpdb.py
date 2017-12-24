import os

os.chdir('./natives_traitees')
liste_pdb = os.listdir()

new_ligne = ''

for chaque_pdb in liste_pdb:
    fichier_pdb = open(chaque_pdb, 'r')
    fichier_refait = open('../'+str(chaque_pdb), 'w')
    #then
    for ligne in fichier_pdb:
        premiere_partie = ligne[0:20]
        deuxieme_partie = ligne[20]
        troisieme_partie = ligne[21:]
        new_ligne = premiere_partie + ' ' + deuxieme_partie + troisieme_partie
        print(new_ligne)
        fichier_refait.write(new_ligne)
        
    fichier_pdb.close()
    fichier_refait.close()
        
