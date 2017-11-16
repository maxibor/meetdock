#!/usr/bin/env python

import math, string



########################################
#         PARSING TOOLS
########################################



def parsePDBMultiChains(infile, charge = 1, chargeFromInfile = False, bfactor = False, CG = False) :
    """ purpose: to parse a pdb file (infile)
        input: PDB file
        output: a dico dPDB which contains for each atom of each residue of
        each chain, its corresponding 3D coordinates. Please take a look to
        the code to understand the structure of the dico.

    """

    # lecture du fichier PDB 
    f = open(infile, "r")
    lines = f.readlines()
    f.close()


    # var init
    chaine = True
    firstline = True
    prevres = None
    dPDB = {}
    dPDB["reslist"] = []
    dPDB["chains"] = []
    
    # parcoure le PDB   
    for line in lines :
        if (line[0:4] == "ATOM") or ((line[0:6] == "HETATM") and ( (string.strip(line[17:20]) == "MET") or  (string.strip(line[17:20]) == "MSE") )) :
            chain = line[21]
            if not chain in dPDB["chains"] :
                dPDB["chains"].append(chain)
                dPDB[chain] = {}
                dPDB[chain]["reslist"] = []
            curres = "%s"%(line[22:27]).strip()
            resnum = "%s"%(line[22:26]).strip()
            if not curres in dPDB[chain]["reslist"] : # first time we encounter it
                dPDB[chain]["reslist"].append(curres)
                dPDB[chain][curres] = {}
                dPDB[chain][curres]["resname"] = string.strip(line[17:20])
                dPDB[chain][curres]["atomlist"] = []
                #dPDB[chain][curres]["atomlistTowrite"] = []
                alternateoccupancy = None #"%s"%(line[16:17])
                occupancy = "%s"%(line[16:17]) 
                if occupancy != " " :
                    alternateoccupancy = occupancy
                

            else: # this is not a new residue
                occupancy = "%s"%(line[16:17])

                if occupancy != " " and alternateoccupancy == None : # means we are in the first alternate location of that residue
                    alternateoccupancy = occupancy
            
            if CG : # means we are parsing a CG model so we have to treat the CSE atomtypes which can be redondant in terms of name the same res
                atomtype = "%s_%s"%(string.strip(line[6:11]), string.strip(line[12:16]))
            else:
                atomtype = string.strip(line[12:16])
            
            #if not atomtype in dPDB[chain][curres]["atomlist"] :
            if occupancy == alternateoccupancy  or occupancy == " " : # means this atom corresponds to the first rotamer found in the PDB for this residue

                #if CG :
                    #dPDB[chain][curres]["atomlistTowrite"].append(atomtype.split("_")[1]) # necessary for the writing later
                
                dPDB[chain][curres]["atomlist"].append(atomtype)
                dPDB[chain][curres][atomtype] = {}
                dPDB[chain][curres][atomtype]["x"] = float(line[30:38])
                dPDB[chain][curres][atomtype]["y"] = float(line[38:46])
                dPDB[chain][curres][atomtype]["z"] = float(line[46:54])
                dPDB[chain][curres][atomtype]["id"] = line[6:11].strip()
                if bfactor == True :
                    dPDB[chain][curres][atomtype]["bfactor"] = float(line[60:67].strip())
                #if chargeFromInfile == True :
                #    dPDB[chain][curres][atomtype]["charge"] = float(line[60:67])
                #else :
                #    dPDB[chain][curres][atomtype]["charge"] = charge


            dPDB[chain][curres]["resnum"] = resnum
            #dPDB[chain][curres]["inser"] =  "%s"%(line[26:27])
 

    return dPDB


#################################################
#           WRITING TOOLS
#################################################


def writePDB(dPDB, filout = "out.pdb", bfactor = False) :
    """purpose: according to the coordinates in dPDB, writes the corresponding PDB file.
       If bfactor = True, writes also the information corresponding to the key bfactor
       of each residue (one key per residue) in dPDB.
       input: a dico with the dPDB format
       output: PDB file.
    """

    fout = open(filout, "w")

    for chain in dPDB["chains"]:
        for res in dPDB[chain]["reslist"] :
            for atom in dPDB[chain][res]["atomlist"] :
                if bfactor :
                    fout.write("ATOM  %5s  %-4s%3s %s%4s    %8.3f%8.3f%8.3f  1.00%7.3f X X\n"%(dPDB[chain][res][atom]["id"], atom, dPDB[chain][res]["resname"],chain, res,dPDB[chain][res][atom]["x"], dPDB[chain][res][atom]["y"],dPDB[chain][res][atom]["z"],dPDB[chain][res]["bfactor"] ))
                else:
                    fout.write("ATOM  %5s  %-4s%3s %s%4s    %8.3f%8.3f%8.3f  1.00  1.00 X X\n"%(dPDB[chain][res][atom]["id"], atom, dPDB[chain][res]["resname"],chain, res,dPDB[chain][res][atom]["x"], dPDB[chain][res][atom]["y"],dPDB[chain][res][atom]["z"] ))
                    
    fout.close()


def initBfactor(dPDB):
    """purpose: initiation of the bfactor key for each residue
       input: a dico with the dPDB format
    """

    for chain in dPDB["chains"]:
        for res in dPDB[chain]["reslist"]:
            dPDB[chain][res]["bfactor"] = 0


            
def generateFastPDB(x, y, z, res = "GEN", atomname = "X", atomid = 1, resid = 1, chain = " ", bfactor = ""):
    """ //// DEBUG FUNCTION ////
        purpose: creates a mini dico dPDB for one atom and its 3D coordinates.
        The idea is to call after the writePDB(my_mini_dico) in order to visualize
        with Pymol the coordinates of the corresponding atom.
        input: x, y, z (3D coordinates of the atom we want to visualize)
        output: a mini dPDB dico for one atom
        usage: my_mini_dico = generateFastPDB(xi, yi, zi) 

    """

    dPDB = {}
    dPDB["chains"] = [chain]
    dPDB[chain] = {}
    dPDB[chain]["reslist"] = [resid]
    dPDB[chain][resid] = {}
    dPDB[chain][resid]["atomlist"] = [atomname]
    dPDB[chain][resid][atomname] = {}
    dPDB[chain][resid][atomname]["id"] = atomid
    dPDB[chain][resid]["resname"] = res
    dPDB[chain][resid][atomname]["x"] = x
    dPDB[chain][resid][atomname]["y"] = y
    dPDB[chain][resid][atomname]["z"] = z
    if bfactor != "":
        dPDB[chain][resid][atomname]["bfactor"] = bfactor

    return dPDB



#####################################################
#         3D MANIPULATION TOOLS
#####################################################





def rotate(x,y,z,x0,y0,z0,alpha,beta,gamma):
    """purpose: rotation of the atom with coords (x, y, z) according to the angles alpha, beta, gamma
       input:   x, y, z  the 3D coordinates of the point to rotate
                x0,y0,z0 the coordinates of the center of rotation (i.e. center of mass of the object we want to rotate)
                alpha, beta, gamma, the angles of the rotation
       output:  (x3i,y3i,z3i) the final coordinates in the initial referential """
    

    # centering according to the center of rotation
    x1i=x-x0
    y1i=y-y0
    z1i=z-z0

    # computing cos and sin of each angle
    c_a=math.cos(alpha)
    s_a=math.sin(alpha)

    c_b=math.cos(beta)
    s_b=math.sin(beta)

    c_g=math.cos(gamma)
    s_g=math.sin(gamma)


    # applying rotation
    x3i = (c_a*c_b*c_g-s_a*s_g)*x1i + (-c_a*c_b*s_g-s_a*c_g)*y1i + c_a*s_b*z1i 
    y3i = (c_a*s_g+s_a*c_b*c_g)*x1i + (-s_a*c_b*s_g+c_a*c_g)*y1i + s_a*s_b*z1i
    z3i = -s_b*c_g*x1i + s_b*s_g*y1i + c_b*z1i 

    # back to the input referential
    x3i = x3i + x0
    y3i = y3i + y0
    z3i = z3i + z0

    return ((x3i,y3i,z3i))




def spherical2CartCoord(ori, R, phi, theta):
    """purpose: from the coords of a center considered as the origin (ori) (tupple), the R distance between the 2 points
       (ori and atom for which we want to compute the cartesian coords)
       and a couple of angles phi, theta defining the position of the atom of interest,
       returns the coords of this atom (cartesian coords).
       input: ori (tupple corresponding to the 3D coords of the origin from which the spherical coords of
       the atom of interest have been defined)
              R distance between ori and the atom of interest
              phi, theta, angles defining the position of the atom of interest according to ori (spherical coordinates)
       output: cartcoords, a tupple containing the 3D cartesian coords xi, yi, zi of the atom of interest       
    """

    # computing x,y,z the 3D coords (relative to ori)
    z = math.cos(theta)*R
    x = math.sin(theta)*math.cos(phi)*R
    y = math.sin(phi)*math.sin(theta)*R

    # back to the original referential, storing in cartcoords
    cartcoords = (ori[0]+x, ori[1]+y, ori[2]+z) 
    
    return  cartcoords


def coord2spherical(ori, coordi):
    """purpose: from the 3D cartesian coordinates of an atom of interest (coordi) and
       those of a point considered as the origin (ori), computes its corresponding
       spherical coordinates according to the origin.
       input: ori (tupple corresponding to the cartesian coords of the origin)
              coordi (tupple corresponding to the cartesian coords of the input atom)
       output: spherical coords (R, phi, theta) of the input atom relative to ori       
    """

    

    x = coordi[0] - ori[0]
    y = coordi[1] - ori[1]
    z = coordi[2] - ori[2]

    R = math.sqrt(x*x + y*y + z*z)
    theta = math.acos(z/R)

    # phi is given in [0:2pi]
    phi = 2*math.pi + math.atan2(y,x)       

    return R, phi, theta



