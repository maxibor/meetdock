#!/usr/bin/env python3

import numpy as np
import pandas as pd
import math
from numpy.fft import *


def multi_mat(rec_grid, lig_grid):
    res = np.matmul(rec_grid, lig_grid)
    res = res.sum()
    # res = res.real
    return(res)



if __name__ == "__main__":
    print("nothing to print")
