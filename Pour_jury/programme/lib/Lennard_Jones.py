#!/usr/bin/env python3
try:
    from lib import pdbtools as pdbt
    from lib import pdb_resdepth as resd
    from lib import matrice_distances as distm
except:
    import pdbtools as pdbt
    import pdb_resdepth as resd
    import matrice_distances as distm



# The function takes the distance matrix as argument and gives the Lennard-Jones potential as result

def lennard_jones(dist_matrix, sigma=3.9, epsilon=10):

    '''
        Calculating Lennard-Jones potential

        INPUT:
               input1(Dictionary): Distances dictionary. Output of calc_distance_matrix() function
               input2 (Float): sigma value for Lennard-Jones function. Default value: 3.9
               input3 (Int): epsilon value for Lennard-Jones function. Default value: 10
        OUPUT:
               result(Float): Lennard-Jones energy value for the complex

    '''

    energy = 0

    for dist in dist_matrix.values():
        frac = pow((sigma/dist),6)
        part_energy = 4*epsilon*(pow(frac,2) - frac)
        energy += part_energy

    return energy


if __name__ == "__main__":

    filename = sys.argv[1]
    structure = pdbt.read_pdb(filename)
    depth = resd.calculate_resdepth(structure, filename)
    dist_matrix = distm.calc_distance_matrix(structure, depth, chain_recp, chain_lig)
    lennard_jones(dist_matrix)
