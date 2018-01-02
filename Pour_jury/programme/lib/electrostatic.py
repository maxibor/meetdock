#!/usr/bin/env python3

import sys, math

try:
    from lib import pdbtools
    from lib import matrice_distances
    from lib import pdb_resdepth

except:
    import pdbtools
    import matrice_distances
    import pdb_resdepth

def amino3to1(resid):
    codes = {
    "ALA":"A",
    "ILE":"I",
    "LEU":"L",
    "PRO":"P",
    "VAL":"V",
    "PHE":"F",
    "TRP":"W",
    "TYR":"Y",
    "ASP":"D",
    "GLU":"E",
    "ARG":"R",
    "HIS":"H",
    "LYS":"K",
    "SER":"S",
    "THR":"T",
    "CYS":"C",
    "MET":"M",
    "ASN":"N",
    "GLN":"Q",
    "GLY":"G"
    }
    return(codes[resid])


def calc_charge(resid, pH):
    """
        Computes charge of a residue
        INPUT:
            - resid(str) 1 letter code of residue
            - pH(float) pH for charge calculation
        OUTPUT:
            - charge(float) charge of the amino acid
    """
    # print(resid)
    # resid_letter = amino3to1(resid[1])
    resid_letter = resid

    resPka = {
    "Y":[+1,10.46],
    "H":[-1,6],
    "C":[1,8.5],
    "D":[-1,4.4],
    "Z":[-1,4.4],
    "K":[+1,10],
    "R":[1,12]
    }

    qi = resPka[resid_letter][0]
    pKa = resPka[resid_letter][1]
    charge = qi/(1+10**(qi*(pH-pKa)))
    return(charge)

def calc_electrostat(charge1, charge2, distance):
    """
        Compute electrostatic energy between two residues
        INPUT:
            - charge1(float) charge of residue 1
            - charge2(float) charge of residue 2
        OUTPUT:
            - res(float) electrostatic energy
    """
    epsr = 80
    eps0 = 885418782*(10**12)
    res = ((charge1*charge2)/(epsr*distance)) * (1/(4*math.pi*eps0))
    return(res)


def electrostatic(inter_resid_dict, pH = 7):
    """
        Computes sum of electrostatic energies between ligand and receptor
        INPUT:
            - inter_resid_dict(dict) dict of distances between residues at
            interface
            - pH(float) pH for charge calculation. Default = 7
        OUTPUT:
            -

    """
    elec_sum = 0
    electro_amino = ["Y","H","C","D","Z","K","R"]
    for akey in inter_resid_dict.keys():
        residcode1 = amino3to1(akey[0][1])
        residcode2 = amino3to1(akey[1][1])
        if (residcode1 in electro_amino) and (residcode2 in electro_amino):
            # print(residcode1, residcode2), inter_resid_dict[akey]
            charge1 = calc_charge(residcode1, pH)
            charge2 = calc_charge(residcode2, pH)
            elec_sum += calc_electrostat(charge1=charge1, charge2=charge2, distance = inter_resid_dict[akey])
    return(elec_sum)




if __name__ == "__main__":
    """
    Usage for testing
        electrostatic.py path/to/complex.pdb recepChain1,recepChainN ligChain1,ligChainN
    """
    myfile = sys.argv[1]
    recepChain = sys.argv[2].split(",")
    ligChain = sys.argv[3].split(",")
    my_struct = pdbtools.read_pdb(myfile)
    depth_dict = pdb_resdepth.calculate_resdepth(structure=my_struct, pdb_filename=myfile)
    inter_resid = matrice_distances.calc_distance_matrix(structure=my_struct, depth= depth_dict, chain_R=recepChain, chain_L=ligChain)
    myElectro = electrostatic(inter_resid_dict=inter_resid, pH=7)
    print(myElectro)
