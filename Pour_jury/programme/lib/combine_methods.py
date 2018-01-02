#!/usr/bin/env python3

import sys
try:
    from lib import pdbtools
    from lib import pdb_resdepth
    from lib import matrice_distances
    from lib import Lennard_Jones
    from lib import electrostatic
    from lib import shape_complement
    from lib import knowledge
except:
    import pdbtools
    import pdb_resdepth
    import matrice_distances
    import Lennard_Jones
    import electrostatic
    import shape_complement
    import knowledge

#Shut up plz biopython
import warnings
from Bio import BiopythonWarning
warnings.simplefilter('ignore', BiopythonWarning)

def combine_score(pdbfile, recepChain, ligChain, statpotrun = True, vdwrun = True, electrorun = True, shaperun = True, pH = True, depth = "msms", dist = 8.6):
    combined_dict = {}
    my_struct = pdbtools.read_pdb(pdbfile)
    depth_dict = pdb_resdepth.calculate_resdepth(structure=my_struct, pdb_filename=pdbfile, method= depth)
    distmat = matrice_distances.calc_distance_matrix(structure=my_struct, depth= depth_dict, chain_R=recepChain, chain_L=ligChain, dist_max=dist, method = depth)

    combined_dict["pdb"] = pdbfile.split("/")[-1]
    if statpotrun == True:
        statpot = knowledge.parse_distance_mat(distmat, method=["glaser"])
        combined_dict["statpot"] = statpot
    if vdwrun == True:
        vdw = Lennard_Jones.lennard_jones(dist_matrix=distmat)
        combined_dict["vdw"] = vdw
    if electrorun == True:
        electro = electrostatic.electrostatic(inter_resid_dict=distmat, pH =pH)
        combined_dict["electro"] = electro
    if shaperun == True:
        shape = shape_complement.runshape(structure=my_struct, recepChain=recepChain, depth_dict=depth_dict, ligChain=ligChain, method = depth)
        combined_dict["shape"] = shape
    # foldx = TOADD




    return(combined_dict)


if __name__ == '__main__':
    myfile = sys.argv[1]
    recepChain = sys.argv[2].split(",")
    ligChain = sys.argv[3].split(",")
    mydict = combine_score(pdbfile=myfile, recepChain=recepChain, ligChain=ligChain)
    print(mydict)
