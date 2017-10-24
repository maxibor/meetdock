from Bio.PDB import *

def residue_depth():
	p = PDBParser()
	structure = p.get_structure('X', '2za4.pdb')
	model = structure[0]
	rd = ResidueDepth(model, '2za4.pdb')


residue_depth()
