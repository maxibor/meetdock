#!/usr/bin/env python3

from Bio.PDB.PDBParser import PDBParser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
from collections import OrderedDict
import sys, math
from fft import init_grid, fill_grid, fill_grid2, make_fft
import pdb_resdepth


def read_pdb(filename):
    """
        READs PDB FILE with BioPython
        INPUT:
            PDB path/filename(str)
        OUTPUT:
            structure(BioPython Structure object)
    """
    parser = PDBParser(PERMISSIVE=1)
    pdbid = filename.split(".")[0]
    structure = parser.get_structure(pdbid, filename)
    return(structure)

def pdb_data_extractor(structure, chainId, depth_dict, depthCutoff):
    """
    COMPUTES RESIDUE POSITIONS AND DEPTH from Structure object
    INPUT:
        structure(BioPython Structure object)
        chainId(str) chain for which to compute residue positions and depth
        depth_dict(dict) Dictionary of residue depth generated by calculate_resdepth()
        depthCutoff(float) depth Cutoff for surface determination
    OUPUT:
        df(pandas dataframe) positions of CB/CA and RESIDUE DEPTH (to add)
            x(list) x position of residues (CA or CB)
            y(list) y position of residues (CA or CB)
            z(list) z position of residues (CA or CB)
            resdepth(list) residue depth, 1 if at surface, else -1
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
    resdepth = []
    for model in structure:
        for chain in model:
            if chain.get_id() == chainId :
                for residue in chain:
                    if "GLY" in residue.get_resname():
                        thisDepth = pdb_resdepth.resdepth_to_fft(residue = residue, cutoff = depthCutoff, mydict = depth_dict)
                        thisResname = residue.get_resname()+str(residue.get_full_id()[3][1])+residue.get_full_id()[2]

                        for atom in residue:
                            # if atom.get_name() == "CA":
                            posx = int(atom.get_coord()[0])
                            x.append(posx)
                            posy = int(atom.get_coord()[1])
                            y.append(posy)
                            posz = int(atom.get_coord()[2])
                            z.append(posz)
                            resdepth.append(thisDepth)
                            resname.append(thisResname)

                    elif residue.get_resname() in amino:
                        thisDepth = pdb_resdepth.resdepth_to_fft(residue = residue, cutoff = depthCutoff, mydict = depth_dict)
                        thisResname = residue.get_resname()+str(residue.get_full_id()[3][1])+residue.get_full_id()[2]

                        for atom in residue:
                            # if atom.get_name() == "CB":
                            posx = int(atom.get_coord()[0])
                            x.append(posx)
                            posy = int(atom.get_coord()[1])
                            y.append(posy)
                            posz = int(atom.get_coord()[2])
                            z.append(posz)
                            resdepth.append(thisDepth)
                            resname.append(thisResname)

    df = pd.DataFrame(x, columns = ["x"], index = resname)
    df["y"] = y
    df["z"] = z
    df["resdepth"] = resdepth
    return(df)









def pdb_fft(structure, recepChain, ligChain, depth_dict, depthCutoff):
    """
        READs PDB FILE AND COMPUTES RESIDUE POSITIONS AND DEPTH
        INPUT :
            PDB path/filename(str)
            recepChain(list) list of receptors chain(str)
            ligChain(list) list of ligand chain(str)
            depth_dict(dict) Dictionary of residue depth generated by calculate_resdepth()
            depthCutoff(float) depth Cutoff for surface determination

        OUTPUT :
            list of pandas dataframe (1 for receptor, 1 for ligand): positions of CB/CA and RESIDUE DEPTH
                x(list) x position of residues (CA or CB)
                y(list) y position of residues (CA or CB)
                z(list) z position of residues (CA or CB)
                resdepth(list) residue depth, 1 if at surface, else -1
    """
    receptor = []
    ligand = []
    for model in structure:
        for chain in model:
            if chain.get_id() in recepChain:
                receptor.append(pdb_data_extractor(structure = structure, chainId = chain.get_id(), depth_dict = depth_dict, depthCutoff = depthCutoff))
            elif chain.get_id() in ligChain:
                ligand.append(pdb_data_extractor(structure = structure, chainId = chain.get_id(), depth_dict = depth_dict, depthCutoff = depthCutoff))
    receptorData = pd.concat(receptor)
    ligandData = pd.concat(ligand)
    return([receptorData, ligandData])




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
    df["x"] = df["x"].map(int)
    df["y"] = df["y"].map(int)
    df["z"] = df["z"].map(int)
    return(df)

def init_dict(L):
    """
        INITIALIZE A DICT OF KEYS (X,Y,Z) OF ZEROS OF LENGTH L
        INPUT:
            L(int) length of the grid of size L*L*L
        OUPUT:
            thisDict(dict) of keys (X,Y,Z) initialized at 0

    """
    thisDict = OrderedDict()
    for x in np.arange(0,L):
        for y in np.arange(0,L):
            for z in np.arange(0,L):
                thisDict[(x,y,z)] = 0
    return(thisDict)

def coords_to_dict(coords):
    """
        TRANSFORMS COORDS TO DICT
        INPUT:
            coords(pd.dataframe) of columns (x,y,z, depth)
        OUPUT:
            thisDict(dict) of keys(X,Y,Z) of value depth
    """
    thisDict = {}
    for i in range(0,len(coords.index)):
        thisDict[(coords.iloc[i,0],coords.iloc[i,1],coords.iloc[i,2])] = coords.iloc[i,3]
    return(thisDict)

def match_dict(zero_dict, coord_dict):
    """
        FILL DICT FROM init_dict() WITH DEPTH VALUES
        INPUT:
            zero_dict(dict) of keys (X,Y,Z) initialized at 0
            coord_dict(dict) of keys(X,Y,Z) of value depth
        OUTPUT:
            zero_dict(dict) of keys (X,Y,Z) of value depth
    """
    for akey in coord_dict.keys():
        # print(akey)
        zero_dict[akey] = coord_dict[akey]
    return(zero_dict)

def dict_to_mat(grid_dict, L):
    """
        TRANSFORM DICT FROM match_dict() FUNCTION TO NUMPY ARRAY
        INPUT:
            grid_dict(dict) of keys(X,Y,Z) of value depth
        OUTPUT:
            grid(np.array) of columns (x,y,z,depth)
    """
    x = []
    y = []
    z = []
    resloc = []
    grid = np.zeros((L,L,L), dtype=complex)
    for key in grid_dict.keys():
        grid[key[0]][key[1]][key[2]] = grid_dict[key]
    return(grid)

if __name__ == "__main__":
    resolution = 5
    depthCutoff = 4
    recepChain = ["A","B"]
    ligChain = ["C","D"]
    # filename = "./2ZA4.pdb"
    filename = sys.argv[1]
    pdb_structure = read_pdb(filename)
    depth_dict = pdb_resdepth.calculate_resdepth(structure=pdb_structure, pdb_filename=filename)

    data = pdb_fft(structure=pdb_structure, recepChain = recepChain, ligChain = ligChain, depth_dict = depth_dict, depthCutoff = depthCutoff)
    receptor = data[0]
    ligand = data[1]
    theComplex = pd.concat([receptor, ligand])
    # receptor
    grid_parameters=get_grid_parameters(x=theComplex.iloc[:,0], y=theComplex.iloc[:,1], z=theComplex.iloc[:,2])

    rec_coords = scale_coords(receptor, grid_parameters= grid_parameters, margin = resolution)
    lig_coords = scale_coords(ligand, grid_parameters= grid_parameters, margin = resolution)

    zero_dict = init_dict(L=grid_parameters[0])

    rec_dict = coords_to_dict(rec_coords)
    lig_dict = coords_to_dict(lig_coords)

    rec_grid_dict = match_dict(zero_dict=zero_dict, coord_dict=rec_dict)
    lig_grid_dict = match_dict(zero_dict=zero_dict, coord_dict=lig_dict)


    rec_grid = dict_to_mat(grid_dict=rec_grid_dict, L=grid_parameters[0])
    # df = pd.Dataframe, rec_grid
    lig_grid = dict_to_mat(grid_dict=lig_grid_dict, L=grid_parameters[0])
    # print(grid_parameters[0][1][0])
    # print(lig_grid)
    print("computing FFT")
    score_matrix = make_fft(rec_grid=rec_grid, lig_grid=lig_grid, L=grid_parameters[0])
    print(score_matrix)
    # print(score_matrix.shape)



    # print(grid_parameters)
    # cmap = cm.get_cmap(name='bwr')
    # colors = ['white','green','red']
    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # ax.scatter(xs=rec_grid.iloc[:,0], ys=rec_grid.iloc[:,1], zs=rec_grid.iloc[:,2], color = cmap(rec_grid.iloc[:,3]), alpha = resolution/100)
    # ax.scatter(xs=rec_grid.iloc[:,0], ys=rec_grid.iloc[:,1], zs=rec_grid.iloc[:,2], cmap = matplotlib.colors.ListedColormap(colors), alpha = resolution/100)

    # ax.scatter(xs=rec_coords.iloc[:,0], ys=rec_coords.iloc[:,1], zs=rec_coords.iloc[:,2], c = "red")
    # plt.show()

    #ligand

    # grid_parameters=get_grid_parameters(x=theComplex.iloc[:,0], y=theComplex.iloc[:,1], z=theComplex.iloc[:,2])
    # lig_coords = scale_coords(ligand, grid_parameters= grid_parameters)
    # lig_mygrid = init_grid(N=grid_parameters[0], mesh_size = resolution)
    # print(grid_parameters)
    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # ax.scatter(xs=lig_mygrid.iloc[:,0], ys=lig_mygrid.iloc[:,1], zs=lig_mygrid.iloc[:,2], c = "blue", alpha = resolution/100)
    # ax.scatter(xs=lig_coords.iloc[:,0], ys=lig_coords.iloc[:,1], zs=lig_coords.iloc[:,2], c = "green")
    # plt.show()
