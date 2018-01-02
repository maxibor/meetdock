#Fait fonctionner le programme de A à Z

#Un mode 'Démo' déjà préconfiguré
    #Sorties dans ./out/ (trois répertoires: sampling, results, summary)
#Sinon:

    #Demande à l'utilisateur le chemin vers le récepteur et le chemin vers le ligand
    #Demande à l'utilisateur le chemin de sortie
    #Crée dans un dossier de sortie trois sous-dossiers "sampling", "results", "summary" et affiche les 10 premiers résultats

import os

def do_samplings(receptorpath='./data/1j5prec.pdb', ligandpath='./data/1j5plig.pdb', outputdir='./out/', nbrot=10, nbx=3, nby=3, nbz=3):

    print('The sampling will be done using TEAM6 naive software')
    print('Receptor: {}\nLigand: {}\noutputdir: {}\nnbrot: {}\nnbx: {}\nnby: {}\nnbz: {}'.format(receptorpath.split('/')[-1], ligandpath.split('/')[-1], outputdir, nbrot, nbx, nby, nbz))

    answer = ''
    current_path = os.getcwd()
    sampl6path = current_path + '/lib/sampling6/Tools'


    cmd = 'python3 '+sampl6path+'/confsGenerator.py '+'-r '+ receptorpath +' -l '+ ligandpath +' -p '+sampl6path+' -nbPt '+ str(nbrot)+" -XRota "+str(nbx)+" -YRota "+str(nby)+" -ZRota "+str(nbz)+" -minimize False"+" -jet False"

    answer = os.system(cmd)
    if answer != 0:
        raise ValueError('Unexpected error while doing the sampling')


if __name__ == '__main__':

    current_path = os.getcwd() 
    sampl6path = current_path + '/lib/sampling6/Tools'


    default = True
    minimize = False

    receptorpath = os.getcwd()+'/data/1j5prec.pdb'
    ligandpath = os.getcwd()+'/data/1j5plig.pdb'
    outdir = current_path+'/out/'
    choix = ''

    print('*****WELCOME TO MEETDOCK AZ*****\n*This will do a naive sampling and then score it through our knowledge-based, electrostatic and VDW calculations altogether combined with machine learning (Random Forrest).\n*See our report for more details about how the model has been trained. \n>>> Be carefull: Parsing your arguments has not been implemented yet !\n\n')

    while choix != 'y' and choix != 'n':
        choix = input('If you want to run the demo, press [y], else press [n]')

    if choix == 'y':
        default = True
        

    elif choix == 'n':

        choix = ''

        receptorpath = input('Enter a correct path to your receptor\' pdb')
        ligandpath = input('Enter a correct path to your receptor\'s pdb')
        outdir = input('Enter the outputdir')
        nbrot = input('Enter a number of ligand rotations (default:3)')
        xrot = input('Enter a number of x rotations')
        yrot = input('Enter a number of y rotations')
        zrot = input('Enter a number of z rotations')
        while minimize != 'y' and minimize != 'n':
            minimize = input('Do you want to use the minimizer MaxDo ? (y/n)')

        if minimize == 'y':
            minimize = True

        elif minimize == 'n':
            minimize = False

    #Whatever the choice

    os.system('cd '+outdir+'\n'+'rm -rf *')

    os.system('mkdir -p '+outdir+'/sampling')
    os.system('mkdir -p '+outdir+'/results')
    os.system('mkdir -p '+outdir+'/summary')

    if default == True:
        print('Starting the demo: All your results will show up in ./out/ . On a decently recent computer you can expect ~ 3 mn of computation time')
        do_samplings() #All values to default
    elif default == False:
        do_samplings(receptorpath=receptorpath, ligandpath=ligandpath,outputdir=outputdir, nbrot=nbrot, nbx=nbx, nby=nby)

    receptorname = receptorpath.split('/')[-1]
    ligandname = ligandpath.split('/')[-1]

    sampl6outdir = sampl6path + '/Results/pdb/'+receptorname+'/'

    os.chdir(current_path+'/lib/sampling6/Minimizer/')
    os.system('python clean.py')

    os.chdir(sampl6outdir)
    liste_samples = os.listdir()

    #Déplacement vers MaxDo... -_-'
    if minimize == True:
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

        os.chdir(outdir+'/sampling/')



    elif minimize == False:

    #Si pas de minimiseur, juste déplacer vers la sortie
        for elt in liste_samples:
            os.system('mv '+str(elt)+' '+str(outdir)+'sampling/'+str(elt))

        os.chdir(outdir+'/sampling/')

#Puis réunifier les PDB avec récepteur = Chaine A et Ligand = Chaine B

    liste_ligands = os.listdir()


    for ligand in liste_ligands:
        ligandid = ligand.replace('rota', '.').split('.')[-2]
        filinreceptor = open(receptorpath, 'r')
        filinligand = open(ligand, 'r')
        filout = open(ligandname.replace('.pdb', '')+'_'+ligandid+'.pdb', 'w')

        for ligne in filinreceptor:
            if ligne.split()[0].strip() == 'ATOM':
                newligne = ligne[0:21]+'A'+ligne[22:]
                filout.write(newligne)

        del (ligne)

        for ligne in filinligand:
            if ligne.split()[0].strip() =='ATOM':
                newligne = ligne[0:21]+'B'+ligne[22:]
                filout.write(newligne)

        filinreceptor.close()
        filinligand.close()
        filout.close()

        os.system('rm '+str(ligand))

    os.chdir(current_path)

    os.system('python meetdock ./out/sampling/'+' '+'-depth naccess') #Lancer meetdock vers le répertoire
