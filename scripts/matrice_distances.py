#!/usr/bin/env python3

import pdb2grid as pdbg
import pdb_resdepth as resd
import re
import math


def calc_distance_matrix(pdb, depth, chain_R, chain_L):

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
                coord = get_coord(key, pdb)
                if coord != None:
                    recepteur[key] = coord
            else:
                coord = get_coord(key, pdb)
                if coord != None:
                    ligand[key] = coord

    #Calculating distances
    for rkey, rval in recepteur.items():
        for lkey, lval in ligand.items():
            dist = math.sqrt(pow((rval[0]-lval[0]),2)+pow((rval[1]-lval[1]),2)+pow((rval[2]-lval[2]),2))
            if dist <= 8.6:
                pair = (rkey, lkey)
                interactions[pair] = dist      
    
    return interactions


def get_coord(aa, pdb):

    ''' Parse a PDB file to get the atoms coordinates
    '''

    file_ = open(pdb)
    chain = aa[0]
    code= aa[1]
    position = aa[2]
    coord = None
    
    if code == "GLY":
        for line in file_:
            res = re.match(r'ATOM.*CA.*'+code+'.*'+chain+'.*'+str(position)+'.*', line)
            if res != None:
                coord = [float(line[30:38].strip()),float(line[38:46].strip()),float(line[46:54].strip())]
    else:
        for line in file_:
            res = re.match(r'ATOM.*CB.*'+code+'.*'+chain+'.*'+str(position)+'.*', line)
            if res != None:
                coord = [float(line[30:38].strip()),float(line[38:46].strip()),float(line[46:54].strip())]
    file_.close()
    if coord != None:
        return coord
    return  

###### MAIN ########

structure = pdbg.read_pdb("1a2k.pdb")
depth = resd.calculate_resdepth(structure, "1a2k.pdb")
dist_matrix = calc_distance_matrix("1a2k.pdb", depth, ["A", "B"],["C", "D", "E"])


