#DELEVOYE Guillaume
#15/11/17

#Juste le script qu'on a utilisé avec Francois pour renommer une partie des samplings des profs de manière plus pratique

import os

liste_fichiers = os.listdir(os.getcwd())

try:
    liste_fichiers.remove('script.py')
    liste_fichiers.remove('translate.py')
except:
    print("ERREUR")

try:
    for rep in liste_fichiers:
        os.system("cp ./script.py ./"+str(rep)+"/script.py")
        os.system("python3 ./"+str(rep)+"/script.py")
except:
    print("c'est pas grave")
