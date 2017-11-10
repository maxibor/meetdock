#!/usr/bin/env python3

import numpy as np
import pandas as pd
import math
from numpy.fft import *


def make_fft(rec_grid, lig_grid, L):
    # tmp = ((1/L**3) *ifftn(np.matmul(ifftn(rec_grid),fftn(lig_grid))))
    tmp = ((1/L**3) *ifftn(np.dot(ifftn(rec_grid),fftn(lig_grid))))
    sc = tmp.real - tmp.imag
    return(sc)



if __name__ == "__main__":
    print("nothing to print")
