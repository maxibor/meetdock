def amino3to1(resid):
    codes = {
    "ALA":"A",
    "ILE":"I",
    "LEU":"L",
    "PRO":"P",
    "VAL":"V",
    "PHE":"F",
    "TRP":"W",
    "TYR":"Y",
    "ASP":"D",
    "GLU":"E",
    "ARG":"R",
    "HIS":"H",
    "LYS":"K",
    "SER":"S",
    "THR":"T",
    "CYS":"C",
    "MET":"M",
    "ASN":"N",
    "GLN":"Q"
    }
    return(codes[resid])


def calc_charge(resid, pH):
    """
        Computes charge of a residue
        INPUT:
            - resid(str) 1 letter code of residue
            - pH(float) pH for charge calculation
        OUTPUT:
            - charge(float) charge of the amino acid
    """

    resid_letter = amino3to1(resid[1])

    resPka = {
    "Y":[+1,10.46],
    "H":[-1,6],
    "C":[1,8.5],
    "D":[-1,4.4],
    "Z":[-1,4.4],
    "K":[+1,10],
    "R":[1,12]
    }

    qi = resPka[resid_letter][0]
    pka = resPka[resid_letter][1]
    charge = qi/(1+10**(qi*(pH-pKa)))
    return(charge)

def calc_electrostat(charge1, charge2, distance):
    """
        Compute electrostatic energy between two residues
        INPUT:
            - charge1(float) charge of residue 1
            - charge2(float) charge of residue 2
        OUTPUT:
            - res(float) electrostatic energy
    """
    epsr = 80
    eps0 = 885418782*(10**12)
    res = ((charge1*charge2)/(epsr*distance)) * (1/(4*math.pi*eps0))
    return(res)


def electrostatic(inter_resid_dict, pH):
    """
        Computes sum of electrostatic energies between ligand and receptor
        INPUT:
            - inter_resid_dict(dict) dict of distances between residues at
            interface
            - pH(float) pH for charge calculation
        OUTPUT:
            -

    """
    elec_sum = 0
    for akey in inter_resid_dict.keys():
        residcode1 = amino3to1(akey[0][1])
        residcode2 = amino3to1(akey[1][1])
        charge1 = calc_charge(residcode1, pH)
        charge2 = calc_charge(residcode2, pH)
        elec_sum += calc_electrostat(charge1=charge1, charge2=charge2, distance = inter_resid_dict[akey])
    return(elec_sum)


if __name__ == "__main__":
    filename = sys.argv[1]
    pdb_structure = read_pdb(filename)
    depth_dict = pdb_resdepth.calculate_resdepth(structure=pdb_structure, pdb_filename=filename)
    # TODO then distance matrix and cutoff from Paula
    
