def parse_foldx_output(filename):
    """Parse un fichier de sortie foldx et récupère les infos intéressantes, qu'il retourne en dictionnaire (clé = Nom, valeur = score):

    Ex:

    BackHbond       =               -181.18
    SideHbond       =               -40.87
    Energy_VdW      =               -298.93
    Electro         =               -9.72
    Energy_SolvP    =               394.94
    Energy_SolvH    =               -391.17
    Energy_vdwclash =               31.98
    energy_torsion  =               9.11
    backbone_vdwclash=              112.33
    Entropy_sidec   =               150.39
    Entropy_mainc   =               394.26
    water bonds     =               0.00
    helix dipole    =               -0.14
    loop_entropy    =               0.00
    cis_bond        =               0.00
    disulfide       =               0.00
    kn electrostatic=               -0.41
    partial covalent interactions = 0.00
    Energy_Ionisation =             1.30
    Entropy Complex =               0.00
    Total          = 				  59.55
    """
    
    liste_mots = ['BackHbond',
    'SideHbond', 
    'Energy_VdW',
    'Electro',         
    'Energy_SolvP',
    'Energy_SolvH',
    'Energy_vdwclash',
    'energy_torsion', 
    'backbone_vdwclash',
    'Entropy_sidec',  
    'Entropy_mainc',
    'waterbonds',
    'helixdipole',
    'loop_entropy',
    'cis_bond',
    'disulfide',
    'knelectrostatic',
    'partialcovalentinteractions ',
    'Energy_Ionisation',
    'EntropyComplex',
    'Total']
    
    output_dict = {}
    
    fichier = open(filename, "r")
    
    for ligne in fichier:
        try:
            if ligne.replace(" ", "").split("=")[0] in liste_mots:
                newligne = ligne.replace(" ","")
                cle = newligne.split("=")[0]
                valeur = float(newligne.split("=")[1][0:-1])
                output_dict[cle] = valeur
        except IndexError:
            print("Erreur:"+str(ligne))    
    return output_dict
    
if __name__ == '__main__':    

    filename = "test.dat"

    dict_sortie = parse_foldx_output(filename)
    for cle in dict_sortie.keys():
        print(cle, dict_sortie[cle])
