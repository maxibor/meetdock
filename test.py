import os

nbrot = 20
nbx = 3
nby = nbx
nbz = nbx

current_path = os.getcwd()

outdir = os.getcwd()+'/out/'

os.chdir(outdir)
os.system('mkdir -p results')
os.system('mkdir -p summary')
os.system('mkdir -p sampling')
os.chdir(current_path)

receptorpath = os.getcwd()+('/data/1j5prec.pdb')
receptorname = receptorpath.split('/')[-1]

ligandpath = os.getcwd()+('/data/1j5plig.pdb')
ligandname = ligandpath.split('/')[-1]

sampl6path = current_path + '/lib/sampling6/Tools'
sampl6outdir = sampl6path + '/Results/pdb/'+receptorname+'/'

os.chdir(current_path+'/lib/sampling6/Minimizer/')
os.system('clean.py')

os.chdir(sampl6path)

cmd = 'python3 '+sampl6path+'/confsGenerator.py '+'-r '+ receptorpath +' -l '+ ligandpath +' -p '+sampl6path+' -nbPt '+ str(nbrot)+" -XRota "+str(nbx)+" -YRota "+str(nby)+" -ZRota "+str(nbz)+" -minimize False"+" -jet False"

os.system(cmd)

os.chdir(sampl6outdir)
liste_samples = os.listdir()

#Déplacement vers MaxDo... -_-'

for elt in liste_samples:

    os.system('mv '+str(elt)+' '+sampl6path+'/../Minimizer/Proteins/'+str(elt))

os.chdir(current_path+'/lib/sampling6/Minimizer/')


#Lancement du minimiseur

del (elt) #Pour recommencer la boucle

for elt in liste_samples:
    if elt != receptorname:
        os.system('runMini.py -rec '+receptorname+' -lig '+elt)

os.chdir('pdb_mini')

#Déplacement vers l'outdir final du programme

liste_mini = os.listdir()
for pdb in liste_mini:
    os.system('mv '+str(pdb)+' '+str(outdir)+'sampling/'+str(pdb))


