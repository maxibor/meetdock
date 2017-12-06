#!/usr/bin/env python3

from lib import pdbtools as pdbt
from lib import pdb_resdepth as resd
import re
import math
import sys
import numpy
from Bio.PDB.PDBParser import PDBParser

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
            if dist <= dist_max:
                pair = (rkey, lkey)
                interactions[pair] = dist
    #print(interactions)

    return interactions

def get_matrix_aa_propensions(method):
    ''' Reads a file containing the propensity value for a given method and
        returns its matrix.
    '''

    # Path to change according after having set the final folder containing
    # propensity values from the different methods.
    path_file = "/Users/ilyesabdelhamid/Desktop/M2/Meet-U/contact_propensities/"+method
    mat = []
    with open(path_file, 'r') as input:
        for i,line in enumerate(input):
            if i > 2:
                mat.append([float(val) for val in line.split()])

    arr_aa = numpy.array(mat)

    return arr_aa

def parse_distance_mat(interaction, method):

    ''' Parse the set of interactions between a residue from the receptor and
        a residue from the ligand. Write and attribute in a file a propensity
        value (coming from different method) for each interaction. The user has
        to enter the list of interaction with at least one method.
    '''

    aa_key = ['ILE', 'VAL', 'LEU', 'PHE', 'CYS', 'MET', 'ALA', 'GLY', 'THR',
     'SER', 'TRP', 'TYR', 'PRO', 'HIS', 'GLU', 'GLN', 'ASP', 'ASN', 'LYS', 'ARG']
    values = [i for i in range(20)]
    dico = dict(zip(aa_key, values))


    if len(method) == 0:
        sys.exit("Enter one method at least")
    else:
        for m in method:
            if m in ['glaser', 'mezei', 'pons', 'pons_surf', 'cips']:
                mat = get_matrix_aa_propensions(m)
                output_filename = 'score_'+m+'.txt'
                output = open(output_filename, 'a')
                score_tot = 0
                for inter in interaction:
                    chainRec, resiRec, num_resiRec = inter[0]
                    chainLig, resiLig, num_resiLig = inter[1]
                    score = mat[dico[resiRec]][dico[resiLig]]
                    score_tot = score_tot + score
                    output.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(resiRec,
                        chainRec, num_resiRec, resiLig, chainLig, num_resiLig))
                output.write('Total statistical potential : {}\n'.format(score_tot))
                output.close()
            else:
               sys.exit("Enter a valid method")

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
