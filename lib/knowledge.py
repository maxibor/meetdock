import re
import math
import sys
import numpy
from Bio.PDB.PDBParser import PDBParser

try:
    from lib import pdbtools as pdbt
    from lib import pdb_resdepth as resd
except:
    import pdbtools as pdbt
    import pdb_resdepth as resd



import os
lib_path = os.getcwd()

def get_matrix_aa_propensions(method):
    ''' Reads a file containing the interface propensities for a given method and
        returns its matrix.
        INPUT:
            method(str) The method could be one of them : glaser, mezei, pons, pons_surf,
            and cips. Each method gives a matrix 20x20 where each cell contains a propensity value,
            that is, a value that indicates the preference of amino acids i and j to be one in front of the other.
        OUTPUT:
            arr_aa(numpy array) The matrix of interface propensities.
    '''

    script_path = os.path.dirname(os.path.realpath(__file__))
    path_file = script_path+"/../potentiel/"+method
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
        INPUT:
            interaction(dict) dictionary storing the distance (Angstrom) based
            on a cutoff (8.6 Angstroms) between a residue from the receptor and
            a residue from the ligand (keys).
            method(str list) method listed above (cf get_matrix_aa_propensions)
        OUTPUT:
            score_tot(int) sum of all propensity values of each pair of residues
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
                #output_filename = 'score_'+m+'.txt'
                #output = open(output_filename, 'a')
                score_tot = 0
                for inter in interaction:
                    chainRec, resiRec, num_resiRec = inter[0]
                    chainLig, resiLig, num_resiLig = inter[1]
                    score = mat[dico[resiRec]][dico[resiLig]]
                    score_tot = score_tot + score
                    #output.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(resiRec,
                    # chainRec, num_resiRec, resiLig, chainLig, num_resiLig))
                #output.write('Total statistical potential : {}\n'.format(score_tot))
                #output.close()
                return(score_tot)
            else:
               sys.exit("Enter a valid method")
