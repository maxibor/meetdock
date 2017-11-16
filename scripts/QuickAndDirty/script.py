#DELEVOYE Guillaume
#15/11/17

#Juste le script qu'on a utilisé avec Francois pour renommer une partie des samplings des profs de manière plus pratique

import os
import re

liste_fichiers = os.listdir(os.getcwd())

for ancien_nom in liste_fichiers:

    #virer out
    nouveau_nom = ancien_nom.replace("out_","")
    #virer _sol
    nouveau_nom = nouveau_nom.replace("sol_", "")
    
    try:
        #print("mv "+str(ancien_nom)+" "+str(nouveau_nom))
        os.system("mv "+str(ancien_nom)+" "+str(nouveau_nom))
    except:
        os.system("echo \"ERROR:"+str(ancien_nom)+" \" > errors.dat")   
