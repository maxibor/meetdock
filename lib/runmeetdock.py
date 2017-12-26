#!/usr/bin/env python3
import sys, argparse, os
import pandas as pd
try:
    from lib import combine_methods as cm
except:
    import combine_methods as cm
try:
    from joblib import Parallel, delayed
    import multiprocessing
except:
    print("No MultiThreading available, running on single threadself.")


def get_args():
    '''This function parses and return arguments passed in'''
    parser = argparse.ArgumentParser(
        prog='MeetDockOne',
        description='MeetDockOne scores a protein complex docking')
    parser.add_argument('pdbpath', help="path to pdb complex directory")
    parser.add_argument(
        '-shape',
        action="store_true",
        help="compute shape complementarity")
    parser.add_argument(
        '-electro',
        action="store_true",
        help="compute Electrostatic interactions")

    parser.add_argument(
        '-jones',
        action="store_true",
        help="compute Lennard-Jones interactions")

    parser.add_argument(
        '-proba',
        action="store_true",
        help="Compute knowledge based interactions")

    parser.add_argument(
        '-recChain',
        default="A",
        help="receptor Chain ID. If there more than one, separate by a ','. Default = 'A'")

    parser.add_argument(
        '-ligChain',
        default="B",
        help="ligand Chain ID. If there more than one, separate by a ','. Default = 'B'")


    parser.add_argument(
        '-pH',
        default=7,
        type=int,
        help="pH for electrostatic interactions. Default = 7")

    parser.add_argument(
        '-depth',
        default=4,
        type=float,
        help="Threshold for surface residue determination (Angstrom). Default = 4")

    parser.add_argument(
        '-dist',
        default=8.5,
        type=float,
        help="Threshold for interface determination (Angstrom). Default = 8.5")

    parser.add_argument(
        '-thread',
        default=999,
        type=int,
        help="Number of threads for MultiThreading. Default: automatic detection")

    args = parser.parse_args()

    mypath = args.pdbpath
    shape = args.shape
    electro = args.electro
    jones = args.jones
    recChain = args.recChain
    ligChain = args.ligChain
    proba = args.proba
    pH = args.pH
    depth = args.depth
    dist = args.dist
    thread = args.thread



    return(mypath, shape, electro, jones, recChain, ligChain, proba, pH, depth, dist, thread)

def run_meetdock(mypath, thread, shape = True, electro = True, jones = True, recChain = True, ligChain = True, proba = True, foldx = True, pH = 7, depth = 4, dist = 8.6):
    pdbs = os.listdir(mypath)
    pdbs = [i for i in pdbs if i.endswith(".pdb")]
    all_res = []
    try:
        def runpdbs(apdb):
            thepdb = mypath+"/"+apdb
            all_res.append(res)
            print("Computing scores for ", apdb)
            res = cm.combine_score(thepdb, recepChain=recChain, ligChain=ligChain, statpotrun=proba, vdwrun=jones, electrorun=electro, shaperun=shape, pH = pH, depth=depth, dist=dist)
            all_res.append(res)

            # print(apdb, ":", res)

        if thread == 999:
            num_cores = multiprocessing.cpu_count()
        else:
            num_cores = thread
        print("Running on",num_cores, "threads")
        results = Parallel(n_jobs=num_cores)(delayed(runpdbs)(apdb) for apdb in pdbs)

    except:
        for apdb in pdbs:
            thepdb = mypath+"/"+apdb
            print("Computing scores for ", apdb)
            res = cm.combine_score(thepdb, recepChain=recChain, ligChain=ligChain, statpotrun=proba, vdwrun=jones, electrorun=electro, shaperun=shape, pH = pH, depth=depth, dist=dist)
            all_res.append(res)

    mydf = pd.DataFrame(all_res)
    mydf = mydf.set_index('pdb')
    print(mydf.to_string())


if __name__ == "__main__":
    mypath, shape, electro, jones, recChain, ligChain, proba, pH, depth, dist, thread = get_args()
    run_meetdock(mypath=mypath, ligChain="A", recChain="B", shape = shape, electro = electro, jones =jones, proba =proba, pH =pH, dist =dist, depth =depth, thread=thread)
