#DELEVOYE Guillaume
#Installs MEETDOCKONE from the github repository

import os
from urllib.request import urlretrieve

current_path = os.getcwd()

def install_miniconda():
    print('INSTALLING ANACONDA')
    print('Please wait till the end of the download (> 300Mb)')

    try:
        urlretrieve('https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh', 'miniconda3')
        os.system('chmod +x miniconda3 \nbash ./miniconda3')
    except:
        print('An unexpected error occured while downloading miniconda. You should try directly from their website')
        input('')
        exit()

def create_env(conda_path, envname):
    os.system('cd '+str(conda_path)+ '\n ./conda env create -f '+str(current_path)+'/environment.yml')

def rewrite_env(new_name):
    filin = open('environment.yml', 'r')
    filetemp = open('env_temp.yml', 'w')
    for ligne in filin:
        if ligne.split(':')[0] == 'name':
            filetemp.write('name: '+str(envname)+'\n')
        else:
            filetemp.write(str(ligne))

    filetemp.close()
    filin.close()
    os.system('rm environment.yml \n mv env_temp.yml environment.yml')

    
fichier = open('installerconfig', 'r')

for i in range(0,5,1):
    print('\n')

for ligne in fichier:
    if ligne[0] != '/':
        print(ligne, end = '')
    elif ligne[0] == '/':
        break

answer = ''
conda_path = ''
envname = ''

input('>')

while str(answer) not in ['y', 'n', 'Y', 'N']:
    answer = input('DO YOU WANT TO USE AN ALREADY INSTALLED VERSION OF MINICONDA ? [y]/[n] ')

if answer == 'y' or answer == 'Y':
    answer = ''
    while os.path.isdir(str(answer)) == False :
        answer = input('Enter the valid path of your current miniconda path\n> ')
    try:
        newpath = os.path.join(str(answer), 'bin')
        print('********************************************************************************\n PROPER CONDA INSTALLATION FOUND AT: '+str(newpath)+'\n********************************************************************************\n')
        os.system('cd '+str(newpath) + '\n' './conda -V')
        conda_path = str(newpath)
    except:
        print('No conda executable has been found at PATH/bin/conda. Your PATH doesn\'t seem correct. Installation has failed')
        input('')
        exit()

else:
    install_miniconda()
    print('\n\n********************************************************************************\n Miniconda was installed successfully !! \n********************************************************************************\n')
    conda_path = input('Please indicate what is the path you installed miniconda in ? \n > ')
    try:
        newpath = os.path.join(str(conda_path), 'bin')
        print('PROPER CONDA INSTALLATION FOUND AT: '+str(newpath))
        os.system('cd '+str(newpath) + '\n' './conda -V')
        conda_path = str(newpath)
    except:
        print('No conda executable has been found at PATH/bin/conda. Your PATH doesn\'t seem correct. Meetdockone installation has failed')
        input('')
        exit()    

print('CREATION OF YOUR ENVIRONNMENT')

while str(answer) not in ['y', 'n', 'Y', 'N']:
    answer = input('Do you want to create a default env ? [y]/[n] (suggested: [y])')

if answer == 'y' or answer == 'Y':
    envname = 'meetu'
else:
    envname = input('Please enter the name you want to give to your miniconda env: ')

try:
    rewrite_env(envname)
    create_env(conda_path, envname)
    rewrite_env(new_name = 'meetu') #On remet le fichier original
    print('\n********************************************************************************\nEnvironment has been seted up correctly\n********************************************************************************\n')
except:
    rewrite_env(new_name = 'meetu') #On remet le fichier original
    print('An error has occured while we tried to create your env. Installation has failed')
    input('')
    exit()

#Unzip foldx
#Move it in meetuenv

print('****** Installation of foldx in the conda env ******')

try:
    os.system('cd ./lib \n unzip ./foldx.zip -d '+str(current_path)+'/temp/')
    os.system('mv ./temp/foldx '+str(conda_path)+'/../envs/'+str(envname)+'/bin/foldx')
    print('\n******************************************************************************** \n foldx has been successfully installed \n ********************************************************************************\n')
except:
    print('foldx couldn\'t be installed properly... Retry if needed')
    input('')
    exit()
    
print('***** Installation of NACCESS in the conda env *****')

try:
#Copie de NACCESS Dans l'environnement

    os.chdir('./lib/NACCESS/')
    liste_fichiers_naccess = os.listdir()

    for fichier_naccess in liste_fichiers_naccess:
        print('Copying '+str(fichier_naccess)+' to conda env')
        os.system('cp ./'+str(fichier_naccess)+' '+str(conda_path)+'/../envs/'+str(envname)+'/bin/'+str(fichier_naccess))

    os.chdir(current_path)
    print('\n********************************************************************************\nNACCESS has been successfully installed ! \n********************************************************************************\n')

except:
    print('An error has occured while installing naccess in conda env. Please retry')
    input('')
    exit()

#Déplacement de la librairie meetdock dans l'environnement anaconda

print('***** Installation of Meetdock in the conda env')

try:
    os.chdir('./lib')
    liste_meetdock = os.listdir()
    os.chdir('../')

    os.system('mkdir '+str(conda_path)+'/../envs/'+str(envname)+'/lib/python3.6/site-packages/meetdockone/')

    for element in liste_meetdock:
        print('Moving '+str(element)+' to conda env')
        os.system('cp '+str('./lib/'+str(element))+' '+str(conda_path)+'/../envs/'+str(envname)+'/lib/python3.6/site-packages/meetdockone/'+str(element))
    print('Installation of meetdock succeeded !')
except:
    print('FAILED TO INSTALL MEETDOCK IN THE CONDA ENV')
    print('PLease check what happened and retry')
    input('')
    exit()

print(' \n\n ********************************************************************************\n MEETDOCK ONE AND ALL ITS DEPENDENCIES HAVE BEEN INSTALLED SUCCESSFULLY \n********************************************************************************')

for ligne in fichier:
    print(ligne, end = '')

input('')
