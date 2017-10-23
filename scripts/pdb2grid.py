#!/usr/bin/env python3


from Bio.PDB.PDBParser import PDBParser
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys


def read_pdb(filename):
    parser = PDBParser(PERMISSIVE=1)
    pdbid = filename.split(".")[0]
    """
        READs PDB FILE AND COMPUTES RESIDUE POSITIONS AND DEPTH
        INPUT :
            PDB path/filename(str)
        OUTPUT :
            coords(tuple) positions of CB/CA and RESIDUE DEPTH (to add)
                x(list) x position of residues (CA or CB)
                y(list) y position of residues (CA or CB)
                z(list) z position of residues (CA or CB)
                resdepth(list) residue depth (to add)
    """
    x = []
    y = []
    z = []
    resdepth = []
    structure = parser.get_structure(pdbid, filename)
    for model in structure:
        for chain in model:
            for residue in chain:
                if "GLY" in residue.get_resname():
                    for atom in residue:
                        if atom.get_name() == "CA":
                            posx = int(atom.get_coord()[0])
                            x.append(posx)
                            posy = int(atom.get_coord()[1])
                            y.append(posy)
                            posz = int(atom.get_coord()[2])
                            z.append(posz)
                            resdepth.append(0)
                else:
                    for atom in residue:
                        if atom.get_name() == "CB":
                            posx = int(atom.get_coord()[0])
                            x.append(posx)
                            posy = int(atom.get_coord()[1])
                            y.append(posy)
                            posz = int(atom.get_coord()[2])
                            z.append(posz)
                            resdepth.append(0)
    coords = (x, y, z, resdepth)
    return(coords)


def get_grid_parameters(x, y, z, resolution):
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
    L = Lmax - Lmin
    nb_cells = int(L / resolution)
    parameters = (nb_cells, Lmin, Lmax)
    return(parameters)


def map_to_range(x, y, z, resdepth, grid_parameters):
    """
    SCALES RESIDUE COORDINATES
    INPUT:
        x(list) x coordinates of residues
        y(list) y coordinates of residues
        z(list) z coordinates of residues
        grid_parameters(tuple) output of get_grid_parameters() function
    OUTPUT:
        coords(np.ndarray) coordinates of residues scaled to 0-nb_cells
    """

    coords = np.array((x, y, z, resdepth), dtype=int)
    coords[0] = np.interp(coords[0], [grid_parameters[1], grid_parameters[2]], [
                          0, grid_parameters[0]])
    coords[1] = np.interp(coords[1], [grid_parameters[1], grid_parameters[2]], [
                          0, grid_parameters[0]])
    coords[2] = np.interp(coords[2], [grid_parameters[1], grid_parameters[2]], [
                          0, grid_parameters[0]])
    return(coords)


if __name__ == "__main__":
    resolution = 1
    filename = sys.argv[1]
    mypdb = read_pdb(filename=filename)
    coords = map_to_range(x=mypdb[0], y=mypdb[1], z=mypdb[2], resdepth=mypdb[3], grid_parameters=get_grid_parameters(
        x=mypdb[0], y=mypdb[1], z=mypdb[2], resolution=resolution))
    print(coords.shape)

    print(mypdb[3])

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(xs=coords[0], ys=coords[1], zs=coords[2])
    plt.show()
