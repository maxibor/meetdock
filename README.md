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

### Environment - Conda

To ensure the cross-platform reproducibility of this method, we choose to work with a [conda](https://conda.io) environment.

The environment file is available here as [environment.yml](./environment.yml).

#### 1- create the environment from the environment.yml file

`conda env create -f environment.yml`

#### 2- activate the environment

`source activate meetu`


## Quick start

```
$ ./meetdock ./data -recChain A -ligChain B -shape -electro -jones -proba
```
- The dictory `./data` contained pdb complexes.  
- The receptor is Chain A (`-recChain A`).  
- The ligand is Chain B (`-LigChain B`).  
- The following methods will be computed on the complexes :    
    - shape complementarity (`-shape`)
    -electrostatic energy (`-electro`)
    - Leenard-Jones interactions (`-jones`)
    - A knowledge based scoring function (`-proba`)


## Documentation

```
$ ./meetdock -h
usage: MeetDockOne [-h] [-shape] [-electro] [-jones] [-proba] [-foldx]
                   [-recChain RECCHAIN] [-ligChain LIGCHAIN] [-pH PH]
                   [-depth DEPTH] [-dist DIST]
                   pdbpath

MeetDockOne scores a protein complex docking

positional arguments:
  pdbpath             path to pdb complex directory

optional arguments:
  -h, --help          show this help message and exit
  -shape              compute shape complementarity
  -electro            compute Electrostatic interactions
  -jones              compute Lennard-Jones interactions
  -proba              Compute knowledge based interactions
  -recChain RECCHAIN  receptor Chain ID. If there more than one, separate by a
                      ','. Default = 'A'
  -ligChain LIGCHAIN  ligand Chain ID. If there more than one, separate by a
                      ','. Default = 'A'
  -pH PH              pH for electrostatic interactions. Default = 7
  -depth DEPTH        Threshold for surface residue determination (Angstrom).
                      Default = 4
  -dist DIST          Threshold for interface determination (Angstrom).
                      Default = 8.5
```
## Warning  
The file 'data_handler' has been developed in order to performed machine learning. Use ./meetdock for scoring
