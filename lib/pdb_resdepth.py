#!/usr/bin/env python3

from Bio.PDB import *
try:
    from lib import ResidueDepth as msms
    from lib import naccess
except:
    import ResidueDepth as msms
    import naccess

import os

method = "msms"

def calculate_resdepth(structure, pdb_filename):
    '''
        Computes the residue depth for a residue of a PDB from
        Structure object.
        INPUT:
            structure(BioPython Structure object)
            pdb_filename(str) PDB for which it calculates residue depth for each residue.
        OUTPUT:
            mydict(dict) that contains keys which are composed of the chain, three letter code
            and position in chain (all in tuple) for a given residue. Values are comosed of the
            residue depth calculated.
    '''

    model = structure[0]

    if method == "msms":
        print("MSMS running for", pdb_filename)
        rd = msms.ResidueDepth(model, pdb_filename)
        print("MSMS finished with", pdb_filename)
        mydict = {}

        for item in rd.property_list:

            # Create a tuple => (chain, residue3LetterCode, Id)
            residue = (
                        item[0].get_parent().id,    # Chain
                        item[0].get_resname(),      # 3 letter code
                        item[0].get_id()[1]         # Position in chain
                    )
            result = item[1]                        # (ResidueDepth, CalphaDepth)

            mydict[residue] = result
        return mydict
            # Stores everything in a dict

    elif method == "naccess":
        rd = naccess.run_naccess(model = model, pdb_file = pdb_filename)
        rd = process_asa_data(rd[1])
        for key in rd.keys():
            print(rd[key])
            break
    # mydict[residue] = result

    # rd = naccess.run_naccess(model = model, pdb_file = pdb_filename)


    # return mydict

def bfactor_to_resdepth(mydict):
    '''
       This function is a procedure.
       Edit the bfactor column of a pdb file which is replaced with
       the residue depth of the corresponding residue (calculated in
       the function calculate_resdepth.
       INPUT:
           mydict(dict) which contains a residue (chain, three letter code, position in chain - tuple format)
           and its corresponding residue depth.
    '''

    with open('2za4.pdb', 'r') as input:
        with open('2za4_modified.pdb', 'w') as output:
            for line in input:
                if not line.startswith("HETATM"):
                    if line.startswith("ATOM"):
                        _chain = line[21:22].strip()
                        _code = line[17:20].strip()
                        _id = int(line[22:26].strip())
                        values = mydict[(_chain, _code, _id)]
                        edited_line = "{}{:6.2f}{}".format(line[:60], values[0], line[66:])
                        output.write(edited_line)
                    else:
                        output.write(line)



def delete_hetatm(pdb_filename):
    ''' This function is a procedure.
        Removes HETATM lines.
        INPUT:
            pdb_filename(str) PDB file for which HETATM lines
            (water molecules) need to be removed.
    '''
    command = "grep -v 'HETATM' {} > clean_{}".format(pdb_filename, pdb_filename)
    os.system(command)

def resdepth_to_fft(residue, cutoff, mydict):

    res = (residue.get_parent().id, # Chain
           residue.get_resname(),   # 3 letter code
           residue.get_id()[1]      # Position in chain
          )
    if mydict[res][0] < cutoff:        # test on ResidueDepth
        return(1)
    else:
        return(9j)

if __name__=='__main__':
    delete_hetatm("2za4.pdb")
    dico_res = calculate_resdepth('clean_2za4.pdb')
    bfactor_to_resdepth(dico_res)
    resdepth_to_fft('D', 'SER', 89, 4, dico_res)
