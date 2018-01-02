#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 09:29:52 2017

@author: taylor, wanying
"""

import argparse,os,shutil,math,sys
import structureTools_MeetU as st



if __name__ == '__main__':
	DIST_CONTACT=-4 #8 Angstrom

	parser = argparse.ArgumentParser()
	parser.add_argument("-r", help="Chemin vers le pdb du recepteur")
	parser.add_argument("-l", help="Chemin vers le pdb du ligand")
	parser.add_argument("-p", help="Chemin vers le dossier principal du programme")
	parser.add_argument("-nbPt", required=False, default=600, help="Nombre de points de depart")
	parser.add_argument("-XRota", required= False, default=7, help="Nombre d'orientations en un point de depart selon l'axe x")
	parser.add_argument("-YRota", required= False, default=7, help="Nombre d'orientations en un point de depart selon l'axe y")
	parser.add_argument("-ZRota", required= False, default=7, help="Nombre d'orientations en un point de depart selon l'axe z")
	parser.add_argument("-minimize", required=False, default="True", help="Par défaut, les PDB ne sont pas minimisés. Changer à True pour minimisation.")
	parser.add_argument("-jet", required=False, default="False", help="Lance le sampling avec Jet ou naif par défaut.")
	args = parser.parse_args()

	if args.p == None or args.r == None or args.l == None: #si l'un des arguments obligatoires est vide
		parser.print_help()
		parser.exit()

	filename_rec=os.path.basename(args.r)
	filename_lig=os.path.basename(args.l)
	nbPt=int (args.nbPt)
	XRota=int (args.XRota)
	YRota=int (args.YRota)
	ZRota=int (args.ZRota)
	prog_path=args.p
	pathMinimizer=prog_path+"/Minimizer"
	pathResults=prog_path+"/Results"

	print ("######################################################")
	print("Début du sampling naïf :")
	print("######################################################")

	print ("receptor pdb:", filename_rec)
	print ("ligand pdb:",filename_lig)

	#### Vérif '-jet' ####
	if args.jet == "True":
		Jet=True
	elif args.jet =="False":
		Jet=False
	##########################


	#### Vérif '-minimize' ####
	if args.minimize == "True":
		mini=True
	elif args.minimize =="False":
		mini=False

	##########################


	##########################

	recepteur = st.parsePDBMultiChains(args.r)
	ligand = st.parsePDBMultiChains(args.l)

	print ("\n\n######################################################")
	print("Deplacement des proteines à leur position initiales :")
	print("######################################################")
	cdm_origin = st.cdm(recepteur)
	st.cdm(ligand)
	trans_origin = st.translation(recepteur,cdm_origin["x"],cdm_origin["y"],cdm_origin["z"])
	distanceRL = recepteur['cdm']['r']+ligand['cdm']['r']+DIST_CONTACT
	st.translation(ligand,distanceRL,cdm_origin["y"],cdm_origin["z"])
	print("Calcul CDM du recepteur apres translation : "); st.cdm(recepteur,True)
	print("Calcul CDM du ligand apres translation : "); st.cdm(ligand,True)

	#essayer de creer un dossier 'Results'
	try:
		os.mkdir("%s"%pathResults)
	except:
		pass

	#essayer de creer un dossier 'ptDepart' dans le dossier 'Results'
	try:
		os.mkdir("%s/ptDepart"%pathResults)
	except:
		pass

	#dans le dossier 'Results/ptDepart', essayer de supprimer le pdb de point de depart correspondant a la proteine actuellement en traitement (pour enlever la sortie de l'ancienne execution)
	try:
		os.remove("%s/ptDepart/%s_ptDepart.pdb"%(pathResults,filename_rec.split("_")[0]))
	except:
		pass

	#essayer de creer dans le dossier 'Results' un dossier 'pdb' pour stocker les fichiers de sorties non minimises
	try:
		os.mkdir("%s/pdb"%pathResults)
	except:
		pass

	#essayer de supprimer le dossier concernant la proteine actuelle (dossier issu de l'ancienne execution)
	try:
		shutil.rmtree("%s/pdb/%s"%(pathResults,filename_rec.split("_")[0]))
	except OSError:
		pass

	os.mkdir("%s/pdb/%s"%(pathResults,filename_rec.split("_")[0]))

	#ecrire le pdb recepteur (le recepteur positionne a l'origine)
# 	recepteur2 = recepteur
# 	st.translation2(recepteur2,trans_origin[0],trans_origin[1],trans_origin[2])
# 	st.writePDB(recepteur2,filout="%s/pdb/%s/%s"%(pathResults,filename_rec.split("_XX")[0],filename_rec))
	st.writePDB(recepteur,filout="%s/pdb/%s/%s"%(pathResults,filename_rec.split("_")[0],filename_rec))

	print ("\n\n######################################################")
	print("Rotation du ligand autour du récepteur:")
	print("######################################################")


	# Lancement avec ou sans Jet2
	if(Jet==False):
		(phi,theta)=st.GeneratePtDepart(nbPt)
	else:
		print("Lancer JET2")
		print("Le nombre de points de depart selectionné va se rapprocher plus ou moins de 'nbPt' que vous avez choisi")
		print("=========================================================================================================================================")

		#~ os.system('export JET2_PATH="%s/JET2/"'%(prog_path))
		#~ shutil.copyfile(args.r,os.path.join(prog_path,"/JET2"))
		#~ os.system("java -cp $JET2_PATH:$JET2_PATH/jet/extLibs/vecmath.jar jet.JET -c ./JET2/default.conf -i \"./JET2/%s\" -o Results/Jet_Output -p AVJC -r local -a 3 -d chain"%(filename_rec))

		os.environ["JET2_PATH"]="%s/JET2/"%prog_path

		try:
			os.mkdir("%s/Jet_Output"%pathResults)
		except:
			pass

# 		print("running JET2")
		os.system("java -cp $JET2_PATH:$JET2_PATH/jet/extLibs/vecmath.jar jet.JET -c $JET2_PATH/default.conf -i %s -o %s/Jet_Output -p AVJC -r local -a 5 -d chain"%(args.r,pathResults))
# 		print("finished running JET2")

		#InterfaceResidus=st.getInterfaceResidus("%s/Jet_Output/%s/%s_jet.res"%(pathResults,filename_rec.split(".")[0],filename_rec.split(".")[0]))
		InterfaceResidus=st.getInterfaceAtoms("%s/Jet_Output/%s/%s"%(pathResults,filename_rec.split(".")[0],filename_rec.split(".")[0]),recepteur)

		dictest={}
		for chain in InterfaceResidus["chains"]:
			dictest[chain]=InterfaceResidus[chain]["reslist"]

		#(phi,theta)=st.selectPtDepart(nbPt,recepteur,InterfaceResidus[0])
		(phi,theta)=st.GeneratePtDepart(nbPt)
		(phi,theta)=st.selectPtDepartBis(recepteur["cdm"], distanceRL,(phi,theta),args.r, recepteur)
		print(len(phi)," points de départ sélectionnés.")


		#~ try:
			#~ print("./JET2/%s"%(filename_rec))
			#~ os.remove("./JET2/%s"%(filename_rec))
		#~ except OSError:
			#~ pass

		#essayer de creer un dossier 'Jet_Output' dans le dossier 'Results'

		###
		#~ st.selectPtDepart(ligand["cdm"],distanceRL,st.GeneratePtDepart(nbPt), "Results/Jet_Output/%s/%s"%(filename_rec.split(".")[0],filename_rec.split(".")[0]), recepteur)

	coord=(recepteur['cdm']['x'],recepteur['cdm']['y'],recepteur['cdm']['z'])
	cb=0

	pas_alpha=int(math.ceil(360/XRota))
	pas_beta=int(math.ceil(360/YRota))
	pas_gamma=int(math.ceil(360/ZRota))

	list_ptDepart=[]
	for i in range(len(phi)):
		ptDepart=st.spherical2CartCoord((coord[0],coord[1],coord[2]),distanceRL,phi[i],theta[i])
		st.translation(ligand,ptDepart[0],ptDepart[1],ptDepart[2])
		list_ptDepart.append([ptDepart[0],ptDepart[1],ptDepart[2]])
		st.cdm(ligand)
		x0=ligand["cdm"]["x"]
		y0=ligand["cdm"]["y"]
		z0=ligand["cdm"]["z"]
		for alpha in range(0,360,pas_alpha):
			for beta in range(0,360,pas_beta):
				for gamma in range(0,360,pas_gamma):
					#print("num conformation ligand:",cb)
					st.translation(ligand,x0,y0,z0)
					st.cdm(ligand)
					st.selfRotation(ligand,alpha,beta,gamma)
					st.rapproche(recepteur,ligand)
# 					st.translation2(ligand, trans_origin[0],trans_origin[1],trans_origin[2])
					st.addPDB(ligand,cb,filout="%s/pdb/%s/%s_rota%s.pdb"%(pathResults,filename_rec.split("_")[0],filename_lig.split(".")[0],cb))
					cb+=1

					print("*",end='')
# 	st.writePDB(recepteur2,filout="%s/pdb/%s/%s"%(pathResults,filename_rec.split("_")[0],filename_rec))
	#print("%s/pdb/%s/%s"%(pathResults,filename_rec.split("_")[0],filename_rec))
	#ecrire fichier pdb pour les points de depart
	st.ptDepartPDB(list_ptDepart,"%s/ptDepart/%s_ptDepart.pdb"%(pathResults,filename_rec.split("_")[0]))

	#### minimisation des output ####
	if mini == True:
# 		os.system("python3 %s/Tools/loopMini.py -r %s"%(prog_path,filename_rec))
		os.system("python3 %s/loopMini.py -r %s"%(prog_path,filename_rec))
	else:
		print("Traitement terminé !")
	#################################"""

	#tracer le graphe pyplot des points de depart
	# st.graph_ptDepart(list_ptDepart,recepteur)
