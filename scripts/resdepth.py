
from Bio.PDB import *

p = PDBParser()
structure = p.get_structure('X', '2za4.pdb')
model = structure[0]
rd = ResidueDepth(model, '2za4.pdb')

mydict = {}

for item in rd.property_list:

    # Create a tuple => (chain, residue3LetterCode, Id)
    residue = (
                item[0].get_parent().id,      # Chain
                item[0].get_resname(),      # 3 letter code
                item[0].get_id()[1]              # Position in chain
              )
    result = item[1]                                # (ResidueDepth, CalphaDepth)

    # Stores everything in a dict
    mydict[residue] = result

print (mydict)


def calc_depth(depth_dict, residue, thresh):
    depth = depth_dict[residue.get_full_id()[2:4]][1]
    if depth < thresh :
        return(-1)
    else :
        return(1)

    return(depth)
