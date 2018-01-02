#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse,os,shutil,math,sys,glob
import structureTools_MeetU as st

#argument
parser = argparse.ArgumentParser()
parser.add_argument("-r", help="receptor file name PDB")
args = parser.parse_args()
rec=args.r

files=glob.glob("Tools/Results/pdb/%s/*.pdb"%rec.split("_")[0]) #On récupère la liste des pdb dans le dossier Results/pdb/nom_prot
nbfile=len(files)-1 #moins le récepteur
count=0

#on enlève les anciens fichiers pdb existants dans le dossier 'Proteins' du dossier 'Minimizer'
for pdb in glob.iglob("/root/mydisk/sampl6/Codes_sampling/Minimizer/Proteins/*.pdb"):
	os.remove(pdb)

#on copie les fichiers du dossier 'Results/pdb/nom_prot' vers le dossier 'Minimizer/Proteins'
for f in files:
	shutil.copy(f, "/root/mydisk/sampl6/Codes_sampling/Minimizer/Proteins/")

print ("\n\n######################################################")
print("Minimisation :")
print("######################################################")
	
os.chdir("/root/mydisk/sampl6/Codes_sampling/Minimizer")#se deplace dans repertoire 'Minimizer'
#on demarre minimiseur sur des couples de fichiers rec-lig dans 
for lig in glob.iglob("Proteins/*"):
	lig=os.path.basename(lig)
	if(lig!=rec):
		print("ligand:",lig)
		print("receptor:",rec)
		os.system("python2 runMini.py -rec %s -lig %s"%(rec,lig))
		count=count+1
		print("Progression:%s/%s"%(count,nbfile))

docname=rec.split("_")[0]+"_mini" #dossier resultat ayant le nom de proteine
pathResults=os.path.split(os.getcwd())[0]+"/Tools/Results" #chemin vers le dossier 'Results'

#creer un dossier 'pdb_mini' dans le dossier 'Results'
try:
	os.mkdir("%s/pdb_mini"%pathResults)
except:
	pass

#supprimer l'ancien dossier concernant cette proteine	
try:
	shutil.rmtree("%s/pdb_mini/%s"%(pathResults,docname))
except OSError:
	pass

os.mkdir("%s/pdb_mini/%s"%(pathResults,docname))
#on deplace les fichiers du 'Minimizer/pdb_mini' vers 'Results/pdb_mini/nom_prot'
for pdb in glob.iglob("pdb_mini/*.pdb"):
	shutil.move(pdb,"%s/pdb_mini/%s"%(pathResults,docname))




