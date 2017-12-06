#!/usr/bin/env python3

import sys
import pdbtools
import pdb_resdepth
import matrice_distances
import Lennard_Jones
import electrostatic
import shape_complement
import knowledge

def combine_score(pdbfile, recepChain, ligChain):
    combined_dict = {}
    my_struct = pdbtools.read_pdb(pdbfile)
    depth_dict = pdb_resdepth.calculate_resdepth(structure=my_struct, pdb_filename=pdbfile)
    distmat = matrice_distances.calc_distance_matrix(structure=my_struct, depth= depth_dict, chain_R=recepChain, chain_L=ligChain)

    statpot = knowledge.parse_distance_mat(distmat, method=["glaser"])
    vdw = Lennard_Jones.lennard_jones(dist_matrix=distmat)
    electro = electrostatic.electrostatic(inter_resid_dict=distmat)
    shape = shape_complement.runshape(structure=my_struct, recepChain=recepChain, depth_dict=depth_dict, ligChain=ligChain)
    # foldx = TOADD
    combined_dict["statpot"] = statpot
    combined_dict["vdw"] = vdw
    combined_dict["electro"] = electro
    combined_dict["shape"] = shape

    return(combined_dict)


if __name__ == '__main__':
    myfile = sys.argv[1]
    recepChain = sys.argv[2].split(",")
    ligChain = sys.argv[3].split(",")
    mydict = combine_score(pdbfile=myfile, recepChain=recepChain, ligChain=ligChain)
    print(mydict)
