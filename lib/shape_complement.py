#!/usr/bin/env python3

import numpy as np
import pandas as pd
import math, sys
import pdb_resdepth
import pdbtools
from collections import OrderedDict

def pdb_fft(structure, recepChain, ligChain, depth_dict, depthCutoff, resScale):
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
                receptor.append(pdbtools.pdb_data_extractor(structure = structure, chainId = chain.get_id(), depth_dict = depth_dict, depthCutoff = depthCutoff, resScale=resScale))
            elif chain.get_id() in ligChain:
                ligand.append(pdbtools.pdb_data_extractor(structure = structure, chainId = chain.get_id(), depth_dict = depth_dict, depthCutoff = depthCutoff, resScale=resScale))
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

def init_dict(L, resolution):
    """
        INITIALIZE A DICT OF KEYS (X,Y,Z) OF ZEROS OF LENGTH L
        INPUT:
            L(int) length of the grid of size L*L*L
        OUPUT:
            thisDict(dict) of keys (X,Y,Z) initialized at 0

    """
    thisDict = OrderedDict()
    for x in range(0,L, resolution):
        for y in range(0,L, resolution):
            for z in range(0,L, resolution):
                thisDict[(x,y,z)] = 0
    # print(thisDict.keys())
    return(thisDict)

def coords_to_dict(coords):
    """
        TRANSFORMS COORDS TO DICT
        INPUT:
            coords(pd.dataframe) of columns (x,y,z, depth)
        OUPUT:
            thisDict(dict) of keys(X,Y,Z) of value depth
    """
    thisDict = OrderedDict()
    for i in range(0,len(coords.index)):
        thisDict[(coords.iloc[i,0].real,coords.iloc[i,1].real,coords.iloc[i,2].real)] = coords.iloc[i,3]
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
        if akey in zero_dict.keys():
        # print(akey)
            zero_dict[akey] = coord_dict[akey]
    return(zero_dict)

def dict_to_mat(grid_dict, L, resolution):
    """
        TRANSFORM DICT FROM match_dict() FUNCTION TO NUMPY ARRAY
        INPUT:
            grid_dict(dict) of keys(X,Y,Z) of value depth
        OUTPUT:
            grid(np.array) of columns (x,y,z,depth)
    """
    resloc = []
    msize = math.ceil(L/resolution)+1
    grid = np.zeros((msize,msize,msize), dtype=complex)
    for key in grid_dict.keys():
        x = int(key[0]/resolution)
        y = int(key[1]/resolution)
        z = int(key[2]/resolution)
        grid[x][y][z] = grid_dict[key]
    return(grid)

def multi_mat(rec_grid, lig_grid):
    res = np.matmul(rec_grid, lig_grid)
    res = res.sum()
    res = res.real
    return(res)

def runshape(pdbfile, structure, recepChain, ligChain, depth_dict, resolution=2, depthCutoff = 4, resScale = "atom"):
    """
    Wrapper function for the shape complementarity
    INPUT:
        - pbdfile(string) path to pdb complex file
        - structure(BioPython Bio.pdb structure object) Containing receptor and ligand complex
        - recepChain(list) List of receptor chain ids. Ex: ["A","B"]
        - ligChain(list) List of ligand chain ids. Ex: ["C","B"]
        - depth_dict(dictionary) Residue depth dictionary
        - resolution(int) Resolution of the shape complementarity grid in Angstrom. Default = 2
        - depthCutoff(float) Cutoff for defining surface residue in Angstrom. Default = 4
        - resScale(string) Either "atom" or "residue". Scale at which to perform shape complementarity. Default = "atom"
    OUPUT:
        - result(int) Shape complementarity score
    """
    filename = pdbfile.split("/")[-1]

    data = pdb_fft(structure=structure, recepChain = recepChain, ligChain = ligChain, depth_dict = depth_dict, depthCutoff = depthCutoff, resScale= resScale)
    receptor = data[0]
    ligand = data[1]
    theComplex = pd.concat([receptor, ligand])
    grid_parameters=get_grid_parameters(x=theComplex.iloc[:,0], y=theComplex.iloc[:,1], z=theComplex.iloc[:,2])

    rec_coords = scale_coords(receptor, grid_parameters= grid_parameters, margin = resolution)
    lig_coords = scale_coords(ligand, grid_parameters= grid_parameters, margin = resolution)

    zero_dict = init_dict(L=grid_parameters[0], resolution= resolution)

    rec_dict = coords_to_dict(rec_coords)
    lig_dict = coords_to_dict(lig_coords)

    rec_grid_dict = match_dict(zero_dict=zero_dict, coord_dict=rec_dict)
    lig_grid_dict = match_dict(zero_dict=zero_dict, coord_dict=lig_dict)
    #
    #
    rec_grid = dict_to_mat(grid_dict=rec_grid_dict, L=grid_parameters[0], resolution=resolution)
    lig_grid = dict_to_mat(grid_dict=lig_grid_dict, L=grid_parameters[0], resolution=resolution)

    result = multi_mat(rec_grid = rec_grid, lig_grid=lig_grid)
    return(result)

if __name__ == "__main__":
    """
    Usage for testing
        shape_complement.py path/to/complex.pdb recepChain1,recepChainN ligChain1,ligChainN
    """
    myfile = sys.argv[1]
    recepChain = sys.argv[2].split(",")
    ligChain = sys.argv[3].split(",")
    my_struct = pdbtools.read_pdb(myfile)
    depth_dict = pdb_resdepth.calculate_resdepth(structure=my_struct, pdb_filename=myfile)
    tmp = runshape(pdbfile = myfile ,structure = my_struct, recepChain = recepChain, ligChain = ligChain, depth_dict = depth_dict, resolution=2, depthCutoff = 4, resScale = "atom")
    print(tmp)
