#!/usr/bin/env python

import glob, shutil, re, tarfile, subprocess, argparse
import sys, os, time



def writeMini(inlines, receptor, ligand):
    """ Purpose: writes the script for the minimization from the template (wd/templates/runMini.sh) and args: 
             modifies prot names and paths
        Input: template content for the minimizer script stored in inlines, recpetor's name, ligand's name
        Output: runMini.sh 
    """
    if ligand == receptor:
        sep = ""
        ligand = (receptor, "_1")
        ligand = sep.join(ligand)
    outfile = open("%s/minimizer/run_mini/runMini.sh"%(workdir), "w+")
    for line in inlines:
        if line[0:13] == "foreach PROT ":
            outfile.write("foreach PROT (\'\\ls $SEPDIR/%s\')\n"%(receptor))
        elif line[0:13] == "foreach PROTT":
            outfile.write("foreach PROTT (\'\\ls $SEPDIR/%s\')\n"%(ligand))
        #elif line[0:10] == "set SEPDIR":
        #    outfile.write("set SEPDIR = %s/Proteins"%workdir)
        else:
            outfile.write(line)
    outfile.close()
    os.system("chmod +x %s/minimizer/run_mini/runMini.sh"%(workdir))

def writeBuilder(inlines, receptor, ligand):
    """ Purpose: writes the script for the PDB reconstruction from the template (wd/templates/rctrPDB.sh) and args: 
             modifies prot names and paths
        Input: template content for the reconstruction script stored in inlines, recpetor's name, ligand's name
        Output: rctrPDB.sh 
    """
    if ligand == receptor:
        sep = ""
        ligand = (receptor, "_1")
        ligand = sep.join(ligand)
    outfile = open("%s/minimizer/run_builder/rctrPDB.sh"%(workdir), "w+")
    for line in inlines:
        if line[0:13] == "foreach PROT ":
            outfile.write("foreach PROT (%s)\n"%(receptor))
        elif line[0:13] == "foreach PROTT":
            outfile.write("foreach PROTT (%s)\n"%(ligand))
        #elif line[0:11] == "set PROTDIR":
        #    outfile.write("set PROTDIR = %s/Proteins"%workdir)
        else:
            outfile.write(line)
    outfile.close()
    os.system("chmod +x %s/minimizer/run_builder/rctrPDB.sh"%(workdir))


############################ ARGS ################################

parser = argparse.ArgumentParser()
parser.add_argument("-rec", required = True, help = "pdb filename of the receptor protein (please store all the pdb (lig and rec) in Proteins/)")
parser.add_argument("-lig", required = True, help = "pdb filename of the ligand protein (please store all the pdb (lig and rec) in Proteins/)")
#parser.add_argument("-wd", required = False, help = "path to working directory (optional)")
parser.add_argument("-conf", required = False, help = "protein conformation index (optional)")
args = parser.parse_args()

rec = args.rec
lig = args.lig

#if args.wd:
#    workdir = args.wd
#else:
workdir = os.getcwd()

if args.conf:
    conf = args.conf
else:
    conf = 1

############################ END ARGS ################################

#### preparation of executables
os.system("chmod +x %s/minimizer/progs_MAXDo/simulmain.out"%(workdir))
os.system("chmod +x %s/minimizer/progs_MAXDo/Getarea2.out"%(workdir))
os.system("chmod +x %s/minimizer/progs_builder/Interface.out"%(workdir))


#### template file for minimzation
infileMini = open("%s/templates/runMini.sh"%(workdir))
inlinesM = infileMini.readlines()
infileMini.close()

#### template file for reconstruction
infileBuild = open("%s/templates/rctrPDB.sh"%(workdir))
inlinesB = infileBuild.readlines()
infileBuild.close()

#### Creates script for launching minimization and pdb reconstruction
writeMini(inlinesM, rec, lig)
writeBuilder(inlinesB, rec, lig)

#### Executes minimization
os.chdir("%s/minimizer/run_mini/"%(workdir))
print "ready to start minimization1 \n============================\nworking directory:", os.getcwd()
os.system("./runMini.sh")

#### Unfortunately, needs to modify format of output for rctrPDB.sh 
globfile = open("%s/minimizer/run_mini/global.dat"%(workdir), "r")
infile = globfile.readlines()
globfile.close()

newglob = open("%s/minimizer/run_builder/global.dat"%(workdir), "w+")
for line in infile:
    globalelement = line.split()
    linetowrite = ('{0[0]:>5s} {0[1]:>3s} {0[2]:>13s} {0[3]:>12s} {0[4]:>12s} {0[5]:>12s} {0[6]:>12s} {0[7]:>12s} {0[8]:>12s} {0[9]:>12s} {0[10]:>12s}\n'.format(globalelement))
    newglob.write(linetowrite)
newglob.close()

#### Executes pdb reconstruction
os.chdir("%s/minimizer/run_builder/"%(workdir))
print "working directory:", os.getcwd()
os.system("./rctrPDB.sh")

#### Move newly created pdb file to pdb conf directory as well as the global file containing the energy information
recid = os.path.basename(rec).split(".")[0]
print recid
ligid = os.path.basename(lig).split(".")[0]
print ligid
rootrecid = os.path.basename(rec)[:6]
print rootrecid
rootligid = os.path.basename(lig)[:6]
print rootligid

     # PDB
pdbfile = "%s/minimizer/run_builder/pdb_files/%s-%s.min1.pdb"%(workdir, rootrecid, rootligid)   
pdbpath = "%s/pdb_mini/%s_%s_min%s.pdb"%(workdir, recid, ligid, conf)
subprocess.call(["mv", pdbfile, pdbpath])

     # global file
inpath = "%s/minimizer/run_mini/global.dat"%(workdir)
outpath = "%s/global_out/global_%s_%s_min%s.dat"%(workdir, recid, ligid, conf)
subprocess.call(["mv", inpath, outpath])

