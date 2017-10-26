
#It would be nice if from the residue Bio.PDB object, a function call 
#(for example resdepth(residue)) would return the following:

#    -1 if inside a protein
#    1 if at the surface
#    0 if not in a protein nor at a surface


from Bio.PDB import *


p = PDBParser()
structure = p.get_structure('X', '2za4.pdb')
model = structure[0]
rd = ResidueDepth(model, '2za4.pdb')

for item in rd:
    print(item)

'''
for model in structure:
    for chain in model:
        for residue in chain:
           print(rd[residue])
           #print(residue_depth, ca_depth)
           #print(residue)
'''
