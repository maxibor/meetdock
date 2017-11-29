import sys
sys.path.insert(0, "./lib/")

import pdb2grid
import pdb_resdepth
import fft
import electrostatic
import argparse

def get_args():
    '''This function parses and return arguments passed in'''
    parser = argparse.ArgumentParser(
        prog='protDocker',
        description='Docks two protein')
    parser.add_argument('file', help=".pdb entry file")
    parser.add_argument(
        '-argument1',
        action="store_true",
        help="what argument1 does")
    parser.add_argument(
        '-argument2',
        action="store_true",
        help="what argument2 does")
    parser.add_argument(
        '-argument3',
        default=0,
        type=int,
        help="non binary argument description")
    parser.add_argument(
        '-argument4',
        default=5.0,
        type=float,
        help="non binary argument description")
    args = parser.parse_args()

    myfile = args.file
    arg1 = args.argument1
    arg2 = args.argument2
    arg3 = args.argument3
    arg4 = args.argument4


    return(myfile, arg1, arg2, arg3, arg4)

if __name__ == "__main__":
     # do something
     pass
