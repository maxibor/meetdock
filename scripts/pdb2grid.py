#!/usr/bin/env python3


from Bio.PDB.PDBParser import PDBParser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys, math
from fft import init_grid


def read_pdb(filename, calc_depth = False):
    parser = PDBParser(PERMISSIVE=1)
    pdbid = filename.split(".")[0]
    """
        READs PDB FILE AND COMPUTES RESIDUE POSITIONS AND DEPTH
        INPUT :
            PDB path/filename(str)
        OUTPUT :
            df(pandas dataframe) positions of CB/CA and RESIDUE DEPTH (to add)
                x(list) x position of residues (CA or CB)
                y(list) y position of residues (CA or CB)
                z(list) z position of residues (CA or CB)
                resdepth(list) residue depth (to add)
    """
    amino = [
        "ALA",
        "ILE",
        "LEU",
        "PRO",
        "VAL",
        "PHE",
        "TRP",
        "TYR",
        "ASP",
        "GLU",
        "ARG",
        "HIS",
        "LYS",
        "SER",
        "THR",
        "CYS",
        "MET",
        "ASN",
        "GLN"]
    x = []
    y = []
    z = []
    resname = []
    if calc_depth:
        resdepth = []
    structure = parser.get_structure(pdbid, filename)
    for model in structure:
        for chain in model:
            for residue in chain:
                if "GLY" in residue.get_resname():
                    if calc_depth:
                        resdepth.append(0)
                    resname.append(residue.get_resname()+str(residue.get_full_id()[3][1])+residue.get_full_id()[2])
                    for atom in residue:
                        if atom.get_name() == "CA":
                            posx = atom.get_coord()[0]
                            x.append(posx)
                            posy = atom.get_coord()[1]
                            y.append(posy)
                            posz = atom.get_coord()[2]
                            z.append(posz)

                elif residue.get_resname() in amino:
                    if calc_depth:
                        resdepth.append(0)
                    resname.append(residue.get_resname()+str(residue.get_full_id()[3][1])+residue.get_full_id()[2])
                    for atom in residue:
                        if atom.get_name() == "CB":
                            posx = atom.get_coord()[0]
                            x.append(posx)
                            posy = atom.get_coord()[1]
                            y.append(posy)
                            posz = atom.get_coord()[2]
                            z.append(posz)


    if calc_depth :
        df = pd.DataFrame(x, columns = ["x"], index = resname)
        df["y"] = y
        df["z"] = z
        df["resdepth"] = resdepth

    else :
        df = pd.DataFrame(x, columns = ["x"], index = resname)
        df["y"] = y
        df["z"] = z

    return(df)


def get_grid_parameters(x, y, z):
    """
        COMPUTES GRID PARAMETERS FOR FFT
        INPUT:
            x(list) x coordinates of residues
            y(list) y coordinates of residues
            z(list) z coordinates of residues
        OUTPUT:
            nb_cells(int) number of grid cells
            Lmin(int) min X|Y|Z positions
            Lmax(int) max X|Y|Z positions
    """

    Lmax = max(max(x), max(y), max(z))
    Lmin = min(min(x), min(y), min(z))
    L = math.ceil(Lmax) - math.floor(Lmin)
    parameters = (L, Lmin, Lmax)
    return(parameters)


def scale_coords(df, grid_parameters, margin = 5):
    """
    SCALES RESIDUE COORDINATES
    INPUT:
        df(pandas dataframe) output of read_pdb() function
        grid_parameters(tuple) output of get_grid_parameters() function
    OUTPUT:
        df(pandas dataframe) scaled output of read_pdb()
    """
    df.iloc[:,0] = np.interp(df.iloc[:,0], [grid_parameters[1], grid_parameters[2]], [
                          0+margin, grid_parameters[0] - margin])
    df.iloc[:,1] = np.interp(df.iloc[:,1], [grid_parameters[1], grid_parameters[2]], [
                          0+margin, grid_parameters[0] - margin])
    df.iloc[:,2] = np.interp(df.iloc[:,2], [grid_parameters[1], grid_parameters[2]], [
                          0+margin, grid_parameters[0] - margin])
    return(df)



if __name__ == "__main__":
    resolution = 9.2
    # filename = "./2ZA4.pdb"
    filename = sys.argv[1]
    mypdb = read_pdb(filename=filename, calc_depth = True)
    grid_parameters=get_grid_parameters(x=mypdb.iloc[:,0], y=mypdb.iloc[:,1], z=mypdb.iloc[:,2])
    coords = scale_coords(mypdb, grid_parameters= grid_parameters)
    mygrid = init_grid(N=grid_parameters[0], mesh_size = resolution)
    print(grid_parameters)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(xs=mygrid.iloc[:,0], ys=mygrid.iloc[:,1], zs=mygrid.iloc[:,2], c = "blue", alpha = resolution/100)
    ax.scatter(xs=coords.iloc[:,0], ys=coords.iloc[:,1], zs=coords.iloc[:,2], c = "red")
    plt.show()
