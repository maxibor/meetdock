#!/usr/bin/env python3

import pdb2grid as pdbg
import pdb_resdepth as resd
import re
import math
from Bio.PDB.PDBParser import PDBParser

def calc_distance_matrix(structure, depth, chain_R, chain_L):

    ''' Creation of a distance matrix which contais 
        the couples of residues that interacts in de complex 

    '''
   
    recepteur = {}
    ligand = {}
    interactions = {}

    # Searching for surface residues 
    for key,val in depth.items():
        if val[0] <= 4:            
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
            if dist <= 8.6:
                pair = (rkey, lkey)
                interactions[pair] = dist      
    print(interactions)
    return interactions


def struct_coord(aa, structure):

    ''' Searching one atom coordinates

    '''
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
 

###### MAIN ########
structure = pdbg.read_pdb("1a2k.pdb")
depth = resd.calculate_resdepth(structure, "1a2k.pdb")
dist_matrix = calc_distance_matrix(structure, depth, ["A", "B"],["C", "D", "E"])


