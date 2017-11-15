#!/usr/bin/env python3

import numpy as np
import pandas as pd
import math
from numpy.fft import *


def make_fft(rec_grid, lig_grid):
    L = rec_grid.shape[0]
    tmp = ((1/L**3) *ifftn(np.matmul(ifftn(rec_grid),fftn(lig_grid))))
    # tmp = ((1/L**3) *ifftn(np.dot(ifftn(rec_grid),fftn(lig_grid))))
    sc = tmp.real - tmp.imag
    sc = sc.sum()
    # sc = sc.real
    return(sc)

def multi_mat(rec_grid, lig_grid):
    res = np.matmul(rec_grid, lig_grid)
    res = res.sum()
    # res = res.real
    return(res)



if __name__ == "__main__":
    print("nothing to print")
