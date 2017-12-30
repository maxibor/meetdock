#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import os, random, sys
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import operator

########################################
#         PARSING TOOLS
########################################



def parsePDBMultiChains(infile, charge = 1, chargeFromInfile = False, bfactor = False, CG = False) :
	""" purpose: to parse a pdb file (infile)
		input: PDB file
		output: a dico dPDB which contains for each atom of each residue of
		each chain, its corresponding 3D coordinates. Please take a look to
		the code to understand the structure of the dico.

	"""

	# lecture du fichier PDB 
	f = open(infile, "r")
	lines = f.readlines()
	f.close()


	# var init
	chaine = True
	firstline = True
	prevres = None
	dPDB = {}
	dPDB["reslist"] = []
	dPDB["chains"] = []
	
	# parcoure le PDB   
	for line in lines :
		if (line[0:4] == "ATOM") or ((line[0:6] == "HETATM") and ( (str.strip(line[17:20]) == "MET") or  (str.strip(line[17:20]) == "MSE") )) :
			chain = line[21]
			if not chain in dPDB["chains"] :
				dPDB["chains"].append(chain)
				dPDB[chain] = {}
				dPDB[chain]["reslist"] = []
			curres = "%s"%(line[22:27]).strip()
			resnum = "%s"%(line[22:26]).strip()
			if not curres in dPDB[chain]["reslist"] : # first time we encounter it
				dPDB[chain]["reslist"].append(curres)
				dPDB[chain][curres] = {}
				dPDB[chain][curres]["resname"] = str.strip(line[17:20])
				dPDB[chain][curres]["atomlist"] = []
				#dPDB[chain][curres]["atomlistTowrite"] = []
				alternateoccupancy = None #"%s"%(line[16:17])
				occupancy = "%s"%(line[16:17]) 
				if occupancy != " " :
					alternateoccupancy = occupancy
				

			else: # this is not a new residue
				occupancy = "%s"%(line[16:17])

				if occupancy != " " and alternateoccupancy == None : # means we are in the first alternate location of that residue
					alternateoccupancy = occupancy
			
			if CG : # means we are parsing a CG model so we have to treat the CSE atomtypes which can be redondant in terms of name the same res
				atomtype = "%s_%s"%(str.strip(line[6:11]), str.strip(line[12:16]))
			else:
				atomtype = str.strip(line[12:16])
			
			#if not atomtype in dPDB[chain][curres]["atomlist"] :
			if occupancy == alternateoccupancy  or occupancy == " " : # means this atom corresponds to the first rotamer found in the PDB for this residue

				#if CG :
					#dPDB[chain][curres]["atomlistTowrite"].append(atomtype.split("_")[1]) # necessary for the writing later
				
				dPDB[chain][curres]["atomlist"].append(atomtype)
				dPDB[chain][curres][atomtype] = {}
				dPDB[chain][curres][atomtype]["x"] = float(line[30:38])
				dPDB[chain][curres][atomtype]["y"] = float(line[38:46])
				dPDB[chain][curres][atomtype]["z"] = float(line[46:54])
				dPDB[chain][curres][atomtype]["id"] = line[6:11].strip()
				if bfactor == True :
					dPDB[chain][curres][atomtype]["bfactor"] = float(line[60:67].strip())
				#if chargeFromInfile == True :
				#    dPDB[chain][curres][atomtype]["charge"] = float(line[60:67])
				#else :
				#    dPDB[chain][curres][atomtype]["charge"] = charge


			dPDB[chain][curres]["resnum"] = resnum
			#dPDB[chain][curres]["inser"] =  "%s"%(line[26:27])
 

	return dPDB


#################################################
#           WRITING TOOLS
#################################################


def writePDB(dPDB, filout = "out.pdb", bfactor = False) :
	"""purpose: according to the coordinates in dPDB, writes the corresponding PDB file.
	   If bfactor = True, writes also the information corresponding to the key bfactor
	   of each residue (one key per residue) in dPDB.
	   input: a dico with the dPDB format
	   output: PDB file.
	"""

	fout = open(filout, "w")

	for chain in dPDB["chains"]:
		for res in dPDB[chain]["reslist"] :
			for atom in dPDB[chain][res]["atomlist"] :
				if bfactor :
					fout.write("ATOM  %5s  %-4s%3s %s%4s    %8.3f%8.3f%8.3f  1.00%7.3f X X\n"%(dPDB[chain][res][atom]["id"], atom, dPDB[chain][res]["resname"],chain, res,dPDB[chain][res][atom]["x"], dPDB[chain][res][atom]["y"],dPDB[chain][res][atom]["z"],dPDB[chain][res]["bfactor"] ))
				else:
					fout.write("ATOM  %5s  %-4s%3s %s%4s    %8.3f%8.3f%8.3f  1.00  1.00 X X\n"%(dPDB[chain][res][atom]["id"], atom, dPDB[chain][res]["resname"],chain, res,dPDB[chain][res][atom]["x"], dPDB[chain][res][atom]["y"],dPDB[chain][res][atom]["z"] ))
					
	fout.close()

def addPDB(dPDB, modelNum , filout = "out.pdb", bfactor = False) :
	"""purpose: according to the coordinates in dPDB, writes the corresponding PDB file.
	   If bfactor = True, writes also the information corresponding to the key bfactor
	   of each residue (one key per residue) in dPDB.
	   input: a dico with the dPDB format
	   output: PDB file.
	"""

	with open(filout, "a") as fout:
		fout.write("MODEL "+str(modelNum)+"\n")
		for chain in dPDB["chains"]:
			for res in dPDB[chain]["reslist"] :
				for atom in dPDB[chain][res]["atomlist"] :
					if bfactor :
						fout.write("ATOM  %5s  %-4s%3s %s%4s    %8.3f%8.3f%8.3f  1.00%7.3f X X\n"%(dPDB[chain][res][atom]["id"], atom, dPDB[chain][res]["resname"],chain, res,dPDB[chain][res][atom]["x"], dPDB[chain][res][atom]["y"],dPDB[chain][res][atom]["z"],dPDB[chain][res]["bfactor"] ))
					else:
						fout.write("ATOM  %5s  %-4s%3s %s%4s    %8.3f%8.3f%8.3f  1.00  1.00 X X\n"%(dPDB[chain][res][atom]["id"], atom, dPDB[chain][res]["resname"],chain, res,dPDB[chain][res][atom]["x"], dPDB[chain][res][atom]["y"],dPDB[chain][res][atom]["z"] ))
						


def initBfactor(dPDB):
	"""purpose: initiation of the bfactor key for each residue
	   input: a dico with the dPDB format
	"""

	for chain in dPDB["chains"]:
		for res in dPDB[chain]["reslist"]:
			dPDB[chain][res]["bfactor"] = 0


			
def generateFastPDB(x, y, z, res = "GEN", atomname = "X", atomid = 1, resid = 1, chain = " ", bfactor = ""):
	""" //// DEBUG FUNCTION ////
		purpose: creates a mini dico dPDB for one atom and its 3D coordinates.
		The idea is to call after the writePDB(my_mini_dico) in order to visualize
		with Pymol the coordinates of the corresponding atom.
		input: x, y, z (3D coordinates of the atom we want to visualize)
		output: a mini dPDB dico for one atom
		usage: my_mini_dico = generateFastPDB(xi, yi, zi) 

	"""

	dPDB = {}
	dPDB["chains"] = [chain]
	dPDB[chain] = {}
	dPDB[chain]["reslist"] = [resid]
	dPDB[chain][resid] = {}
	dPDB[chain][resid]["atomlist"] = [atomname]
	dPDB[chain][resid][atomname] = {}
	dPDB[chain][resid][atomname]["id"] = atomid
	dPDB[chain][resid]["resname"] = res
	dPDB[chain][resid][atomname]["x"] = x
	dPDB[chain][resid][atomname]["y"] = y
	dPDB[chain][resid][atomname]["z"] = z
	if bfactor != "":
		dPDB[chain][resid][atomname]["bfactor"] = bfactor

	return dPDB



#####################################################
#         3D MANIPULATION TOOLS
#####################################################





def rotate(x,y,z,x0,y0,z0,alpha,beta,gamma):
	"""purpose: rotation of the atom with coords (x, y, z) according to the angles alpha, beta, gamma
	   input:   x, y, z  the 3D coordinates of the point to rotate
				x0,y0,z0 the coordinates of the center of rotation (i.e. center of mass of the object we want to rotate)
				alpha, beta, gamma, the angles of the rotation
	   output:  (x3i,y3i,z3i) the final coordinates in the initial referential """
	

	# centering according to the center of rotation
	x1i=x-x0
	y1i=y-y0
	z1i=z-z0

	# computing cos and sin of each angle
	c_a=math.cos(alpha)
	s_a=math.sin(alpha)

	c_b=math.cos(beta)
	s_b=math.sin(beta)

	c_g=math.cos(gamma)
	s_g=math.sin(gamma)


	# applying rotation
	x3i = (c_a*c_b*c_g-s_a*s_g)*x1i + (-c_a*c_b*s_g-s_a*c_g)*y1i + c_a*s_b*z1i 
	y3i = (c_a*s_g+s_a*c_b*c_g)*x1i + (-s_a*c_b*s_g+c_a*c_g)*y1i + s_a*s_b*z1i
	z3i = -s_b*c_g*x1i + s_b*s_g*y1i + c_b*z1i 

	# back to the input referential
	x3i = x3i + x0
	y3i = y3i + y0
	z3i = z3i + z0

	return ((x3i,y3i,z3i))
	

def spherical2CartCoord(ori, R, phi, theta):
	"""purpose: from the coords of a center considered as the origin (ori) (tupple), the R distance between the 2 points
	   (ori and atom for which we want to compute the cartesian coords)
	   and a couple of angles phi, theta defining the position of the atom of interest,
	   returns the coords of this atom (cartesian coords).
	   input: ori (tupple corresponding to the 3D coords of the origin from which the spherical coords of
	   the atom of interest have been defined)
			  R distance between ori and the atom of interest
			  phi, theta, angles defining the position of the atom of interest according to ori (spherical coordinates)
	   output: cartcoords, a tupple containing the 3D cartesian coords xi, yi, zi of the atom of interest       
	"""

	# computing x,y,z the 3D coords (relative to ori)
	z = math.cos(math.radians(phi))*R
	x = math.sin(math.radians(phi))*math.cos(math.radians(theta))*R
	y = math.sin(math.radians(phi))*math.sin(math.radians(theta))*R

	# back to the original referential, storing in cartcoords
	cartcoords = (ori[0]+x, ori[1]+y, ori[2]+z) 
	
	return  cartcoords


def coord2spherical(ori, coordi):
	"""purpose: from the 3D cartesian coordinates of an atom of interest (coordi) and
	   those of a point considered as the origin (ori), computes its corresponding
	   spherical coordinates according to the origin.
	   input: ori (tupple corresponding to the cartesian coords of the origin)
			  coordi (tupple corresponding to the cartesian coords of the input atom)
	   output: spherical coords (R, phi, theta) of the input atom relative to ori       
	"""
	x = coordi[0] - ori[0]
	y = coordi[1] - ori[1]
	z = coordi[2] - ori[2]

	R = math.sqrt(x*x + y*y + z*z)
	phi = math.degrees(math.acos(z/R))

	theta = math.degrees(math.atan2(y,x))  
	if (theta<0):
		theta=360+theta     

	return R, phi, theta

#Set the center of mass of the protein to a new position
def translation(dPDB, x,y,z):
	x_coef = x - dPDB['cdm']['x']
	y_coef = y - dPDB['cdm']['y']
	z_coef = z - dPDB['cdm']['z']
	#print("déplacement de ",x_coef,y_coef,z_coef)
	for chains in dPDB["chains"]:
		for res in dPDB[chains]["reslist"]:
			for atom in dPDB[chains][res]["atomlist"]:
				dPDB[chains][res][atom]['x']+=x_coef
				dPDB[chains][res][atom]['y']+=y_coef
				dPDB[chains][res][atom]['z']+=z_coef
	
	return([x_coef, y_coef, z_coef])
	
def translation2(dPDB, x_coef,y_coef,z_coef):

	#print("déplacement de ",x_coef,y_coef,z_coef)
	for chains in dPDB["chains"]:
		for res in dPDB[chains]["reslist"]:
			for atom in dPDB[chains][res]["atomlist"]:
				dPDB[chains][res][atom]['x']-=x_coef
				dPDB[chains][res][atom]['y']-=y_coef
				dPDB[chains][res][atom]['z']-=z_coef
				
   
## Ajoute au dictionnaire "a" le centre de masse de la protéine
# @a : dicionnaire d'un fichier pdb
def cdm(dPDB,display=False):
	cdm={'x':0 , 'y':0, 'z':0,'r':0}
	div=0
	
	for chain in dPDB["chains"]:
		for res in dPDB[chain]["reslist"]:
			for atom in dPDB[chain][res]["atomlist"]:
				#print(cdm['x'],"+",dPDB[chain][res][atom]['x'],"=",cdm['x']+dPDB[chain][res][atom]['x'])
				cdm['x']+=dPDB[chain][res][atom]['x']
				cdm['y']+=dPDB[chain][res][atom]['y']
				cdm['z']+=dPDB[chain][res][atom]['z']
				div+=1
	
	#En sortie de boucle, tous les atomes ont été parcourus:
	#print("cdm x calcule:",cdm['x']/div,"avec cdm[x]=",cdm['x'],"sur ",div," atomes." )
	
	cdm['x']=round(cdm['x']/div,10)
	cdm['y']=round(cdm['y']/div,10)
	cdm['z']=round(cdm['z']/div,10)

	
	#Ajout du cdm aux dico de la protéine
	dPDB["cdm"]=cdm
	#Ajout du rayon giratoire de la protéine
	rayonCDM(dPDB)
	if(display==True):
		print(dPDB['cdm'])
	return(dPDB['cdm'])


def cdm_residu(dicoRes):
	cdm={'x':0 , 'y':0, 'z':0,'r':0}
	div=0
	for atom in dicoRes["atomlist"]:
		cdm['x']+=dicoRes[atom]['x']
		cdm['y']+=dicoRes[atom]['y']
		cdm['z']+=dicoRes[atom]['z']
		div+=1

	cdm['x']=round(cdm['x']/div,10)
	cdm['y']=round(cdm['y']/div,10)
	cdm['z']=round(cdm['z']/div,10)
	dicoRes["cdm"]=cdm

	for atom in dicoRes["atomlist"]:
		rayon=distanceAtomes(dicoRes['cdm'],dicoRes[atom])
		if(dicoRes['cdm']['r']<rayon):
			dicoRes['cdm']['r']=rayon
	cdm['r']=round(rayon,10)



## prend en entrée deux atomes (donc les dico d'info des deux atomes) (x,y,z) et retourne la distance entre eux
def distanceAtomes(a,b):
	x1 = a['x']
	y1 = a['y']
	z1 = a['z']

	x2 = b['x']
	y2 = b['y']
	z2 = b['z']
	
	dist= math.sqrt(pow(x1-x2,2)+pow(y1-y2,2)+pow(z1-z2,2))
	return dist



# Rajoute au dico ['cdm'] le rayon maximum entre l'atome le plus éloigné du résidu et le centre de masse
def rayonCDM(dPDB):
	
		for chains in dPDB["chains"]:
			for res in dPDB[chains]["reslist"]:
				for atom in dPDB[chains][res]["atomlist"]:
					rayon=distanceAtomes(dPDB['cdm'],dPDB[chains][res][atom])
					if(dPDB['cdm']['r']<rayon):
						dPDB['cdm']['r']=rayon

#la fonction permettant de rapprocher le ligand au recepteur   
def rapproche(dRecepteur,dLigand):
	"""but: rapprocher le ligand du recepteur (adaptee a toutes formes de proteines)
	input: dRecepteur dictionnaire du recepteur, dLigand dictionnaire du ligand
	"""
	distRL=dRecepteur["cdm"]["r"]+dLigand["cdm"]["r"]
	distLR=dRecepteur["cdm"]["r"]+dLigand["cdm"]["r"]
	magnitude=distanceAtomes(dLigand["cdm"],dRecepteur["cdm"])
	Ar=dRecepteur['cdm']
	Al=dLigand['cdm']
	dist_min=magnitude
	tour=0
	
	while dist_min>8:
		tour=tour+1
		Al_pred=Al
		Ar_pred=Ar
		for chains in dLigand["chains"]:
			for res in dLigand[chains]["reslist"]:
				for atom in dLigand[chains][res]["atomlist"]:
					dist=distanceAtomes(Ar_pred,dLigand[chains][res][atom])
					if(dist<distRL): #recherche l'atome du ligand qui a la plus courte distance avec le centre de masse du recepteur (au 1er tour) ou avec un atome Ar du recepteur trouve au tour precedent
						distRL=dist
						Al={"res":res,"x":dLigand[chains][res][atom]["x"],"y":dLigand[chains][res][atom]["y"],"z":dLigand[chains][res][atom]["z"]} #l'atome du ligand le plus proche du centre de masse du recepteur(au 1er tour) ou le plus proche de l'atome Ar trouve au tour precedent
				
		for chains in dRecepteur["chains"]:
			for res in dRecepteur[chains]["reslist"]:
				for atom in dRecepteur[chains][res]["atomlist"]:
					dist=distanceAtomes(Al_pred,dRecepteur[chains][res][atom])
					if(dist<distLR): #recherche l'atome du recepteur qui a la plus courte distance avec le centre de masse du ligand (au 1er tour) ou avec un atome Al du ligand trouve dans le tour precedent
						distLR=dist
						Ar={"res":res,"x":dRecepteur[chains][res][atom]["x"],"y":dRecepteur[chains][res][atom]["y"],"z":dRecepteur[chains][res][atom]["z"]} #l'atome du recepteur le plus proche du centre de masse du ligand(au 1er tour) ou le plus proche de l'atome Al trouve au tour precedent

		#projection(s) et calcul du norme de(s) vecteur(s)
		if tour==1: # le premier tour, on calcule une distance entre l'atome de recepteur le plus proche de cdm de ligand et l'atome de ligand le plus proche de cdm de recepteur puis la projection sur le vecteur cdm ligand cdm recepteur
			vect_AlAr={"x":Al["x"]-Ar["x"],"y":Al["y"]-Ar["y"],"z":Al["z"]-Ar["z"]} 
			dot_product=vect_AlAr["x"]*dLigand["cdm"]["x"]+vect_AlAr["y"]*dLigand["cdm"]["y"]+vect_AlAr["z"]*dLigand["cdm"]["z"]
			projection={"x":(dot_product/pow(magnitude,2))*dLigand["cdm"]["x"], "y":(dot_product/pow(magnitude,2))*dLigand["cdm"]["y"], "z":(dot_product/pow(magnitude,2))*dLigand["cdm"]["z"]}
			norm=math.sqrt(pow(projection["x"],2)+pow(projection["y"],2)+pow(projection["z"],2))
			dist_min=norm
		else:
			vect_AlAr1={"x":Al["x"]-Ar_pred["x"],"y":Al["y"]-Ar_pred["y"],"z":Al["z"]-Ar_pred["z"]} #vecteur de l'atome du ligand le plus proche de l'atome du recepteur du tour precedent vers l'atome du recepteur du tour precedent
			dot_product1=vect_AlAr1["x"]*dLigand["cdm"]["x"]+vect_AlAr1["y"]*dLigand["cdm"]["y"]+vect_AlAr1["z"]*dLigand["cdm"]["z"]
			projection1={"x":(dot_product1/pow(magnitude,2))*dLigand["cdm"]["x"], "y":(dot_product1/pow(magnitude,2))*dLigand["cdm"]["y"], "z":(dot_product1/pow(magnitude,2))*dLigand["cdm"]["z"]}
			norm1=math.sqrt(pow(projection1["x"],2)+pow(projection1["y"],2)+pow(projection1["z"],2))
			
			vect_AlAr2={"x":Al_pred["x"]-Ar["x"],"y":Al_pred["y"]-Ar["y"],"z":Al_pred["z"]-Ar["z"]} #vecteur de l'atome du recepteur le plus proche de l'atome du ligand du tour precedent vers l'atome du ligand du tour precedent
			dot_product2=vect_AlAr2["x"]*dLigand["cdm"]["x"]+vect_AlAr2["y"]*dLigand["cdm"]["y"]+vect_AlAr2["z"]*dLigand["cdm"]["z"]
			projection2={"x":(dot_product2/pow(magnitude,2))*dLigand["cdm"]["x"], "y":(dot_product2/pow(magnitude,2))*dLigand["cdm"]["y"], "z":(dot_product2/pow(magnitude,2))*dLigand["cdm"]["z"]}
			norm2=math.sqrt(pow(projection2["x"],2)+pow(projection2["y"],2)+pow(projection2["z"],2))

			if norm1<norm2:
				dist_min=norm1
				projection=projection1
			else:
				dist_min=norm2
				projection=projection2

		#deplacement du ligand
		x=dLigand["cdm"]["x"]-projection["x"]
		y=dLigand["cdm"]["y"]-projection["y"]
		z=dLigand["cdm"]["z"]-projection["z"]
		translation(dLigand,x,y,z)
		cdm(dLigand)

#generer les points de depart autour du recepteur
def GeneratePtDepart(P):
	"""But: generer les points de depart selon le fibonacci de sphere (se referer a l'article A.Gonzalez 2009)
		Input:
			P nombre de points au total a generer (un nombre impair est conseille, sinon, un point en moins a la sortie)
		Output: une tuple de liste phi et de liste theta pour les points de depart
	"""
	N=int(math.ceil((P-1)/2))
	phi=[]
	theta=[]
	for i in range(-N,N+1):
		lat=math.degrees(math.asin(float(2*i)/float(P)))+90
		lon=(i%1.618)*(360/1.618)
		phi.append(lat)
		theta.append(lon)
	return (phi,theta)	
	

#Rotation du ligand sur lui même
def selfRotation(ligand, alpha, beta, gamma):
	"""But: Rotation du ligand sur lui même, selon 3 axes (x,y,z) avec les angles alpha, beta, gamma.
			2 angles suffisent pour explorer toutes les possibilités
		Input:
			ligand: le PDB du ligand à faire tourner.
			alpha: angle sur l'axe x
			beta: angle sur l'axe y
			gamma: angle sur l'axe z
		Output: PDB du ligant ayant subit la rotation
	"""
	x0=ligand["cdm"]["x"]
	y0=ligand["cdm"]["y"]
	z0=ligand["cdm"]["z"]
	
	for chains in ligand["chains"]:
		for res in ligand[chains]["reslist"]:
			for atom in ligand[chains][res]["atomlist"]:
				#on fait tourner chaque atom de la molécule par rapport au centre de masse
				new_pos=rotate(ligand[chains][res][atom]["x"], ligand[chains][res][atom]["y"], ligand[chains][res][atom]["z"],x0,y0,z0,math.radians(alpha),math.radians(beta),math.radians(gamma))
				ligand[chains][res][atom]["x"]=new_pos[0]
				ligand[chains][res][atom]["y"]=new_pos[1]
				ligand[chains][res][atom]["z"]=new_pos[2]
		

#creer fichier pdb pour les points de depart
def ptDepartPDB(listPtDepart,filename):
	"""But: ecrire un fichier pdb pour les points de depart
		Input:
			listPtDepart une liste de liste de coordonnees de points de depart
		Output: fichier pdb pour les points de depart
	"""
	cpt=0
	dico={}
	for pos in listPtDepart:
		cpt=cpt+1
		dico=generateFastPDB(pos[0], pos[1], pos[2])
		addPDB(dico,cpt,filout=filename)
		
#prendre les residus de l'interface
def getInterfaceResidus(f,nbC=9):
	"""but : Prendre les residus de l'interface predit par SC3 (inspire par l'article de Hughes Ripoche et al. 2016)
		input : f le fichier '_jet.res', nbC nombre de classes pour classer les residus selon leur SC3
		output : dictionnaire contenant le numero de classe comme cle (classe zero contient les residus ayant SC3 les plus eleves, et les numeros de residus comme valeur
	"""
	dicoResInter={}
	dicoRes={}
	with open(f , 'r') as f:
		first_line = f.readline()
		for line in f:
			if (float(line[14:17])>0.8):
				PC=line[26:32]
				CV=line[18:24]
				SC3=(float(PC)+(1-float(CV)))/2
			dicoRes["%s"%line[4:7].strip()]=SC3
	best=max(dicoRes.values())		
	dicoResInter=createClass(dicoRes,best,nbC)	
	return dicoResInter


#creer des classes
def createClass(dico, bestscore, nbcl) :
	"""but : classer les valeurs d'un dictionnaire en nombre de classes que les utilisateurs souhaitent
	input : dico dictionnaire, bestscore valeur maximale, nbcl nombre de classes
	output : dictionnaire contenant le numero de classe comme cle, et les numeros de residus comme valeur
	"""
	classe={} 
	compteur=nbcl
	seuil=0
	isIn=[]
	while len(classe) != nbcl:
		compteur=compteur-1
		classe[compteur]=[]
		seuil=(nbcl-compteur)*(bestscore/nbcl)
		for key in dico.keys():
			if dico[key] <= seuil:
				if not key in isIn:
					classe[compteur].append(key) #on range le numero du residu
					isIn.append(key)
	return classe


#selectionner les points pour le sampling non naif	
def selectPtDepart(nbPt,recepteur,reslist,seuil=6):
	"""but : selectionner les points de depart pour le sampling non naif
	input : nbPt nombre de points de depart souhaite, recepteur le dictionnaire du recepteur, reslist la liste des residus de classe zero
	output : une liste de phi de points de depart selectionnes et une liste de theta de points de depart selectionnes
	"""
	phiList=[]
	thetaList=[]
	ori=(0,0,0)
	for chain in recepteur["chains"]:
		for res in recepteur[chain]["reslist"]:
			if res in reslist:
				coordi=(float(recepteur[chain][res]["CA"]["x"]),float(recepteur[chain][res]["CA"]["y"]),float(recepteur[chain][res]["CA"]["z"]))
				(R,phi,theta)=coord2spherical(ori,coordi)
				phiList.append(phi)
				thetaList.append(theta)
	proba=((max(phiList)-min(phiList))/180)*((max(thetaList)-min(thetaList))/360) #la proba de trouver un point dans le bon endroit en considerant la selection de phi/theta indpt (methode tres approximative pour savoir combien de points il faut generer pour faire de la selection ensuite)
	nb=math.ceil(nbPt/proba)
	(phi,theta)=GeneratePtDepart(nb)
	phi_ptD=[]
	theta_ptD=[]
	for i in range(len(phiList)): 
		for j in range(len(phi)):
			if phi[j]>=phiList[i]-seuil and phi[j]<=phiList[i]+seuil and theta[j]>=thetaList[i]-seuil and theta[j]<=thetaList[i]+seuil:
				phi_ptD.append(phi[j])
				theta_ptD.append(theta[j])
	return (phi_ptD,theta_ptD)		
			
#################################################
#           Graph tool
#################################################   

#graphe de points de depart
def graph_ptDepart(listPtDepart, recepteur):
	"""But: tracer le graphe de point de depart du ligand autour du recepteur
		Input:
			listPtDepart une liste de liste de coordonnees de points de depart
			recepteur un dictionnaire de recepteur
		Output: graphe en 3D
	"""
	x=[]
	y=[]
	z=[]
	X=[]
	Y=[]
	Z=[]
	for chain in recepteur["chains"]:
		for res in recepteur[chain]["reslist"]:
			for atom in recepteur[chain][res]["atomlist"]:
				X.append(recepteur[chain][res][atom]["x"])
				Y.append(recepteur[chain][res][atom]["y"])
				Z.append(recepteur[chain][res][atom]["z"])
	for pos in listPtDepart: 
		x.append(pos[0])
		y.append(pos[1])
		z.append(pos[2])
	y=np.array(y)
	x=np.array(x)
	z=np.array(z)
	ax = Axes3D(plt.gcf())
	ax.scatter(X,Y,Z, s=30,c="#a569bd",linewidths=0.05)
	ax.scatter(x, y, z,c="yellow")
	plt.show()
	
		
## renvoie le RMSD entre deux proteines pour un atome donnée
# @a : dictionnaire de la premire proteine 
# @b : dictionnaire de la deuxieme proteine
def simple_rmsd(a,b):
	#Atome par défaut CA
	N = 0
	s=0.0
	for chains in a["chains"]:
		for res in a[chains]["reslist"]:
			for atom in a[chains][res]["atomlist"]:
				s+=pow(distanceAtomes(a[chains][res][atom],b[chains][res][atom]),2)
				N+=1
	if(N>0):
		return(math.sqrt(s/N))
	else:
		print("Aucun atome dans le dictionnaire spécifié !")
		#Sinon aucune paire n'a été alignée : retourne None (car division par 0 impossible)


## Fonction qui permettra d'afficher le graphique RMDS vs AA positions (pas de dictionnaire en entrée car temporalité importante) (liste probablement)
# @dic : dictionnaire de couples (clé=idRotation, valeur=RMSD)
# @lType : type de tracer, par defaut en ligne 
def drawRMSD(dic,lType='-',title="A Graph Has No Name."):
	
	listCle=[]
	listVal=[]
	cle=[]
	for j in dic.keys():
		cle.append(j)
		listVal.append(dic[j])
		listCle.append(int(j.split("rota")[1].split(".")[0]))
		
	print ("Le RMSD minimum est:",min(listVal))
	print("La rotation de plus faible RMSD est:",cle[listVal.index(min(listVal))])

	plt.scatter(listCle,listVal)
	plt.title(title)
	plt.ylabel('RMSD(A)')
	plt.xlabel('Rotation')
	print("Dessin terminé !")
	plt.show()
	

## Construit un dictionnaire des RMSD entre les solutions du dossier issu de la minimisation et la vrai solution.
#@path_folder_rota : Le dossier contenant les rotations minimisées
#@path_soluce : le PDB contenant la vrai solution
#@filename_rec: nom du fichier du récepteur (on ne traite pas ce fichier s'il est présent dans le dossier)
def computeRMSD(path_folder_rota, path_soluce, filename_rec=""):
	"""but: Vérifier que notre sampling est suffisament exhaustif, 
	cad on a réussi à généré une solution relativement proche de la vrai solution"""
	if(path_folder_rota[-1:] != "/"):
		path_folder_rota+="/"
		
	soluce = parsePDBMultiChains(path_soluce)
	fics = os.listdir(path_folder_rota)
	dicoRMSD=dict()
	recName = filename_rec

	for i in fics:
		if i != recName:
			rota = parsePDBMultiChains(path_folder_rota+i)
			dicoRMSD[i]=simple_rmsd(rota, soluce)
			
	return dicoRMSD

				
## Extrait la liste des résidus potentiellement à l'interface à partir d'un fichier JET2
# @path : chemin vers le fichier résultat de JET2
# @lig : dictionnaire du ligand ou de la protéine dont on veut regarder les résidus intéressants. 
# @return : dictionnaire de résidus(avec atomes+ (x,y,z) si interface trouvée, None sinon
def getInterfaceAtoms(path, rec): 
	dataJet={}
	liste=[]

	rSeuil=20
	seuilAXS=0.8
	seuilCV=0.5
	seuilPC=0.5


	jetRes=path+"_jet.res"
	#atomeAxs=path+"_atomAxs.res"

	with open(jetRes, 'r') as jetFile:
		for line in jetFile:
			if(line[0:4].strip()!="AA"):
				aa = line[0:4].strip()
				posAA=line[4:8].strip()
				chain=line[8:14].strip()
				axs=float(line[14:18].strip())
				cv=float(line[18:25].strip())
				pc=float(line[25:32].strip())

				if(chain not in dataJet):
					dataJet[chain]=[]
					#liste=[]
				else:
					if(posAA in dataJet):
						print("ERREURE FATALE :",posAA)
					elif(axs>=seuilAXS and cv>=seuilCV and pc>=seuilPC):
						dataJet[chain].append(posAA)
						#liste.append(posAA)
	#print("Liste de Résidus:",dataJet)

	for key in dataJet:
		if(len(dataJet[key])<rSeuil):
			del dataJet[key]
		else:
		#On a détecté plus de 20 résidus dans la liste des résidus qui respectent les conditions
			output={"chains":[], "reslist":[]}

			for chain in rec["chains"]:
				output["chains"].append(chain)
				output[chain]={"reslist":[]}

				rayMax=0
				for res in rec[chain]["reslist"]:
					if (res in dataJet[key]):
						output[chain]["reslist"].append(res)
						output[chain][res]=rec[chain][res]
						cdm_residu(output[chain][res])

						#Sauvegarde tu plus grand rayon
						if(rayMax<output[chain][res]['cdm']['r']):
							rayMax=output[chain][res]['cdm']['r']
						###


						#print(output[chain][res]["cdm"])
				#print("rayMax",rayMax)

		return(output)





## Calcul le projeté orthogonale d'un point M sur une droite passant par les points A et B dans l'espace.
# 0M : point dont on cherche le projeté orthogonale
# @A : point de la droite sur laquelle on projette M
# @B : point de la droite sur laquelle on projette M 
# @return : coordonnées du projeté orthogonal du point M sur la droite (A,B) et la distance entre le point M et le projeté orthogonal.
def popode(M,A,B):
	u={"x":B["x"]-A["x"],"y":B["y"]-A["y"],"z":B["z"]-A["z"]}
	d=-(u["x"]*M["x"])-(u["y"]*M["y"])-(u["z"]*M["z"])
	t=(u["x"]*A["x"]+u["y"]*A["y"]+u["z"]*A["z"]+d)/(-pow(u["x"],2)-pow(u["y"],2)-pow(u["z"],2))

	x=A["x"]+(u["x"]*t)
	y=A["y"]+(u["y"]*t)
	z=A["z"]+(u["z"]*t)

	distM=math.sqrt(pow((M["x"]-x),2)+pow((M["y"]-y),2)+pow((M["z"]-z),2))
	return({"x":x,"y":y,"z":z,"dist":distM})



## Sélectionne les points de départ à proximité des résidus sélectionnés par JET2
#cdm point d'origine
#distance Récepteur-Ligand
#angles liste [[phi],[theta]]
#path_rec : path vers lerécepteur
#dicoRec: dico récepteur
def selectPtDepartBis(cdm, distRL, angles, path_rec, dicoRec):
	listPhi=[]
	listTheta=[]
	k_factor=2  #coefficient multiplicateur du rayon du cylindre de sélection

	root=os.path.split(path_rec)[0]
	nomFic=os.path.basename(path_rec).split(".")[0]
	vect=getInterfaceAtoms(root+"/"+nomFic,dicoRec)

	for i in range(len(angles[0])-1):
		ptDepart=spherical2CartCoord((cdm["x"], cdm["y"], cdm["z"]), distRL,angles[0][i],angles[1][i])
		dictPt={"x":ptDepart[0], "y":ptDepart[1], "z":ptDepart[2]}

		for chain in vect["chains"]:
			for res in vect[chain]["reslist"]:		
				depP=popode(dictPt,vect[chain][res]["cdm"],dicoRec["cdm"])

				if (vect[chain][res]["cdm"]['r']*k_factor)>depP["dist"]:
					if distanceAtomes(dictPt,vect[chain][res]["cdm"])<distanceAtomes(dictPt, dicoRec["cdm"]):
						#le point de départ est en face du résidu on l'enregistre
						listPhi.append(angles[0][i])
						listTheta.append(angles[1][i])
	return((listPhi,listTheta))
	

if __name__ == '__main__':
	path_test="/home/taylor/Documents/MeetU/2017-2018_Equipe6/Codes_sampling/Results/Jet_Output/1AHW_r/1AHW_r.pdb"
	recepteur = parsePDBMultiChains(path_test)
	#print(ligand)
	

	vect = getInterfaceAtoms(path_test.split(".")[0], recepteur)

	if vect==None:
		print("Aucune interface détectée !")
	else:
		print("blabla")
		#print(popode())
	
	#print("Residues at interface are :\n", vect['C']['reslist'])
	
	#Pour exécuter ces lignes il faut avoir les fichiers issus de la minimisation
	#mydico=computeRMSD("/home/taylor/Documents/MeetU/Downloaded/src/pdb_mini","/home/taylor/Documents/MeetU/Downloaded/src/solution/1AHW.pdb", "1AHW_r.pdb")
	#print(mydico)
	#print("La rotation de plus faible RMSD est:",min(mydico))
	#drawRMSD(mydico)
	#M={"x":2,"y":8,"z":-3}
	#A={"x":18,"y":-10,"z":30}
	#B={"x":26,"y":-20,"z":33}
	#vec=popode(M,A,B)
	#print("x:",vec[0],"  y:",vec[1],"  z:",vec[2], "Dist:",vec[3])







	
	
	
