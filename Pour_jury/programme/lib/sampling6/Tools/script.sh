#!/usr/bin/bash

# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 17:19:43 2017

@author: mathildebertrand
@author: taylor.vingadassalon
@author: arnaud.begue
"""

#script qui permet de lancer le logiciel JET2 en ligne de commande
#bash

#Récupération du fichier d'intérêt
path_pdb=$1
nom_pdb=$2
options=$3
#sh script.sh ./1AHW_l_sep.pdb 1AHW_l_sep.pdb AVJC

<<<<<<<
#sh script.sh ../1AHW_l_sep.pdb 1AHW_l_sep.pdb AVJC

=======

>>>>>>>
#chemin d'acces
#export JET2_PATH="../JET2/"

#Copie du fichier à traiter dans le répertoire de travail
cp $path_pdb ../JET2


#cd ../JET2
cd ./JET2
#Création du dossier de sortie
mkdir Jet_Output

java -cp $JET2_PATH:$JET2_PATH/jet/extLibs/vecmath.jar jet.JET -c default.conf -i $nom_pdb -o Jet_Output -p $options -r local -a 3 -d chain

#On déplace le dossier output dans le dossier Results
rm -r ./Results/Jet_Output
mv Jet_Output ./Results/
rm $nom_pdb


