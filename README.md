# MeetDockOne: a scoring method for protein protein docking

<img src="./images/logo.png" width="250">

---

## Authors:  
- [Guillaume Delevoye](https://github.com/GDelevoye)  
- [François Gravey](https://github.com/fgravey)  
- [Ilyes Abdelhamid](https://github.com/IlyesAbdelhamid)  
- [Paula Milan Rodriguez](https://github.com/PaulaMilanRguez)  
- [Maxime Borry](https://github.com/maxibor)  

## Introduction

This scoring method uses the following steps:

- Checking for shape complementarity and steric clashes.
- Knowledge based scoring on amino-acids interactions.
- Electrostatic and Van der Waals interactions scoring.
- Adjusting the weights of the different scoring functions by machine learning.

## Dependancies

- [Conda](https://conda.io/docs/)

## Download

#### 1- download the latest release of MeetDock [here](https://github.com/meetU-MasterStudents/2017-2018_Equipe1/releases/latest)

#### 2- decompress the `.zip` file

`unzip 2017-2018_Equipe1-*`

#### 3- go to MeetDockOne folder

`cd 2017-2018_Equipe1-*`

## Installation

### A- Environment - Conda

To ensure the cross-platform reproducibility of this method, we choose to work with a [conda](https://conda.io) environment.

The environment file is available here as [environment.yml](./environment.yml).

#### 1- create the environment from the environment.yml file

`conda env create -f environment.yml`

#### 2- activate the environment

`source activate meetu`

#### 3- solvant accessible surface (optional)

The default method to compute the solvant accessible surface is [msms](http://mgltools.scripps.edu/packages/MSMS).  
However, it is **really slow** and will **not work for big complexes, but it will run out of the box** and is included in *MeetDockOne*.  

To solve this issue, it is also possible to run *MeetDockOne* with [Naccess](http://wolf.bms.umist.ac.uk/naccess/) (see Documentation section of this readme), a faster and more reliable method.  
To do so, you will first need to [install](http://wolf.bms.umist.ac.uk/naccess/) Naccess yourself.    

The compilation of Naccess requires a special Fortran compiler  that is not available for OS X, therefore, it will only work on Linux (`sudo apt-get install gfortran`).

## Quick start

```
(meetu) user@yourmachine:/home/maxime/meetdockone# ./meetdock  path/to/meetdockone/data -recChain A -ligChain B -shape -electro -jones -proba
```
- The dictory `path/to/meetdockone/data` contains pdb complexes to score.  
- The receptor is Chain A (`-recChain A`).  
- The ligand is Chain B (`-LigChain B`).  
- The following methods will be computed on the complexes :    
    - shape complementarity (`-shape`)
    -electrostatic energy (`-electro`)
    - Leenard-Jones interactions (`-jones`)
    - A knowledge based scoring function (`-proba`)


## Documentation

```
(meetu) user@yourmachine:/path/to/meetdockone# ./meetdock -h
usage: MeetDockOne [-h] [-shape] [-electro] [-jones] [-proba] [-outdir OUTDIR]
                   [-recChain RECCHAIN] [-ligChain LIGCHAIN] [-depth DEPTH]
                   [-pH PH] [-dist DIST] [-thread THREAD]
                   pdbpath

MeetDockOne scores a protein complex docking

positional arguments:
  pdbpath             absolute path to pdb complex directory

optional arguments:
  -h, --help          show this help message and exit
  -shape              compute shape complementarity
  -electro            compute Electrostatic interactions
  -jones              compute Lennard-Jones interactions
  -proba              Compute knowledge based interactions
  -outdir OUTDIR      path to (existing) output directory
  -recChain RECCHAIN  receptor Chain ID. If there more than one, separate by a
                      ','. Default = 'A'
  -ligChain LIGCHAIN  ligand Chain ID. If there more than one, separate by a
                      ','. Default = 'B'
  -depth DEPTH        Method for residue depth/solvant accessibility. [msms |
                      naccess]. Default = msms
  -pH PH              pH for electrostatic interactions. Default = 7
  -dist DIST          Threshold for interface determination (Angstrom).
                      Default = 8.5
  -thread THREAD      Number of threads for MultiThreading. Default: automatic
                      detection
```
