#Fait fonctionner le programme de A à Z
#Demande à l'utilisateur le chemin vers le récepteur et le chemin vers le ligand
#Demande à l'utilisateur le chemin de sortie
#Crée dans un dossier de sortie trois sous-dossiers "sampling", "results", "summary" et affiche les 10 premiers résultats

import os, subprocess

def checkinput(userinput, typeinput):
    '''Return 0 if the output is acceptable'''

    return 0

def do_samplings(receptorpath, ligandpath, outputdir):

    nbrot = 20
    nbx = 3
    nby = nbx
    nbz = nbx

    current_path = os.getcwd()
    sampl6path = current_path + '/lib/sampling6/Tools'

    cmd = 'python3 '+sampl6path+'/confsGenerator.py '+'-r '+ receptorpath +' -l '+ ligandpath +' -p '+sampl6path+' -nbPt '+ str(nbrot)+" -XRota "+str(nbx)+" -YRota "+str(nby)+" -ZRota "+str(nbz)+" -minimize False"+" -jet False"
 			
    try:
        subprocess.check_output(cmd, shell = True)
    except:
        print("Error while running sampl6 on",acomplex)

def minimize(receptorpath, ligandpath, outputdir):
    pass

def do_scoring(outputdir):
    pass

def write_summary(outpudir):
    pass


if __name__ == '__main__':

    current_path = os.getcwd()

    receptorpath = ''
    ligandpath = ''
    outdir = ''

    print('WELCOME TO MEETDOCK AZ\n')

    while checkinput(userinput=receptorpath, typeinput='pdbpath') != 0:
        receptorpath = input('Enter a correct path to your receptor\' pdb')
    while checkinput(userinput=ligandpath, typeinput='pdbpath') != 0:
        ligandpath = input('Enter a correct path to your receptor\'s pdb')
    while checkinput(userinput=outdir, typeinput='outdir') != 0:
        outdir = input('Enter the outputdir')

    os.system('mkdir -p '+outdir+'/sampling")
    os.system('mkdir -p '+outdir+'/results")
    os.system('mkdir -p '+outdir+'/summary")

    do_samplings(receptorpath, ligandpath, outputdir)
    do_scoring(outputdir)
    write_summary(outputdir)
