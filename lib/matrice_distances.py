#!/usr/bin/env python3

try:
    from lib import pdbtools as pdbt
    from lib import pdb_resdepth as resd
except:
    import pdbtools as pdbt
    import pdb_resdepth as resd

import re
import math
import sys
import numpy
from Bio.PDB.PDBParser import PDBParser

method = "naccess"
# method = "msms"

def calc_distance_matrix(structure, depth, chain_R, chain_L, dist_max=8.6):

    """
        Creation of a distance dictionary which contains
        the couples of residues that interacts in de complex

        INPUT:
               input1 (BioPDB Structure): Complex's structure
               input2 (Dictionary): output of calculate_resdepth() function
               input3 (List): Receptor's chains
               input4 (List): Ligand's chains
               input5 (Float): maximum distance between two residues to consider that they interact. Default value: 8.6 A

        OUPUT:
               result(Dictionary): keys (List): Amino acid couples that interacts in the complex
                                   values (int): distance between the two residues
    """


    recepteur = {}
    ligand = {}
    interactions = {}

    if method == "msms":
        cutoff = 4
    elif method == "naccess":
        cutoff = 25

    # Searching for surface residues
    for key,val in depth.items():
        if (val[0] <= cutoff and method == "msms") or (val[0] >= cutoff and method == "naccess"):
            if key[0] in chain_R:
                coord = struct_coord(key, structure)
                if type(coord) != str:
                    recepteur[key] = coord
            else:
                coord = struct_coord(key, structure)
                if type(coord) != str:
                    ligand[key] = coord

    #Calculating distances
    for rkey, rval in recepteur.items():
        for lkey, lval in ligand.items():
            dist = math.sqrt(pow((rval[0]-lval[0]),2)+pow((rval[1]-lval[1]),2)+pow((rval[2]-lval[2]),2))
            if dist <= dist_max:
                pair = (rkey, lkey)
                interactions[pair] = dist
    #print(interactions)

    return interactions

def struct_coord(aa, structure):

    """
        Searching one atom coordinates

        INPUT:
               input1(List): information for one residue
               input2 (BioPDB Structure): Complex's structure
        OUPUT:
               result(List): atom coordinates
    """

    chain = aa[0]
    code= aa[1]
    position = aa[2]
    coord = None

    if code == 'GLY':
        atom = structure[0][chain][int(position)]['CA']

        return atom.get_coord()
    elif code in ['PRO','ALA','VAL','LEU','ILE','MET','CYS','PHE','TYR','TRP','HIS','LYS','ARG','GLN','ASN','GLU','ASP','SER','THR']:
        atom = structure[0][chain][position]['CB']
        return atom.get_coord()
    return 'Error'

if __name__=='__main__':

    structure = pdbt.read_pdb("2za4_modified.pdb")
    depth = resd.calculate_resdepth(structure, "2za4_modified.pdb")
    dist_matrix = calc_distance_matrix(structure, depth, ["A"],["B"])
    parse_distance_mat(dist_matrix, ['glaser', 'pons_surf'])
