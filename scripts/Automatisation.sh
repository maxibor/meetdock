#!/bin/bash

mkdir 'Outputs'
mkdir 'Outputs/foldx_analysis'
cd Data
liste_fichiers='*.pdb'
for fichier in $liste_fichiers
do
	echo "fichier trouve !!! : $fichier" ; 
	./foldx --command=Stability --pdb=$fichier --output-dir='../Outputs/foldx_analysis'
done

cd '../Outputs/foldx_analysis'
ls *.fxout > ../Noms.txt

cd '../../'
python3 parcing.py