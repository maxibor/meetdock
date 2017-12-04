#!/usr/bin/env python3

import pdb2grid as pdbg
import pdb_resdepth as resd
import matrice_distances as distm

# The function takes the distance matrix as argument and gives the Lennard-Jones potential as result

def lennard_jones(dist_matrix, sigma=3.9, epsilon=10):

    ''' Calculating Lennard-Jones potential
    '''

    energy = 0

    for dist in dist_matrix.values():
        frac = pow((sigma/dist),6)
        part_energy = 4*epsilon*(pow(frac,2) - frac)
        energy += part_energy

    return energy
        

if __name__ == "__main__":

    filename = sys.argv[1]
    structure = pdbg.read_pdb(filename)
    depth = resd.calculate_resdepth(structure, filename)
    dist_matrix = distm.calc_distance_matrix(structure, depth, chain_recp, chain_lig)
    lennard_jones(dist_matrix)
