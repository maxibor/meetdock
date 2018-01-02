#DELEVOYE Guillaume
#Installs MEETDOCKONE from the github repository

import os
import sys
from urllib.request import urlretrieve


current_path = os.getcwd()

def install_miniconda():
    print('INSTALLING MINICONDA')
    print('Please wait till the end of the download (> 80Mb)')

    try:
        urlretrieve('https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh', 'miniconda3')
        error = os.system('chmod +x miniconda3 \nbash ./miniconda3')
        if error != 0:
            raise TypeError('Unexpected execution')
    except:
        print('An unexpected error occured while downloading miniconda. You should try directly from their website')
        input('')
        sys.exit(1)

def create_env(conda_path, envname):
    error = os.system('cd '+str(conda_path)+ '\n ./conda env create -f '+str(current_path)+'/environment.yml')
    #if error != 0:
        #raise TypeError('Unexpected execution')


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
    error = os.system('rm environment.yml \n mv env_temp.yml environment.yml')
    if error != 0:
        raise TypeError('Unexpected execution')


    
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
error = 0

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
        error = os.system('cd '+str(newpath) + '\n' './conda -V')

        if error != 0:
            raise TypeError('Unexpected execution')

        conda_path = str(newpath)
    except:
        print('No conda executable has been found at PATH/bin/conda. Your PATH doesn\'t seem correct. Installation has failed')
        input('')
        sys.exit(1)

else:
    try:
        install_miniconda()
        print('\n\n********************************************************************************\n Miniconda was installed successfully !! \n********************************************************************************\n')
    except:
        print('An error occured during miniconda installation')

    conda_path = input('Please indicate what is the path you installed miniconda in ? \n > ')
    try:
        newpath = os.path.join(str(conda_path), 'bin')
        print('PROPER CONDA INSTALLATION FOUND AT: '+str(newpath))
        error = os.system('cd '+str(newpath) + '\n' './conda -V')

        if error != 0:
            raise TypeError('Unexpected execution')

        conda_path = str(newpath)
    except:
        print('No conda executable has been found at PATH/bin/conda. Your PATH doesn\'t seem correct. Meetdockone installation has failed')
        input('')
        sys.exit(1)

print('Installing supplementary required packages') 

print('Updating conda')

try:
    actual_path = os.getcwd()
    os.chdir(conda_path)
    print(conda_path)

    error = os.system('./conda update --all')

    if error != 0:
        raise TypeError('Unexpected execution')

    error = os.system('./conda install -c msarahan libcxxabi')

    if error != 0:
        raise TypeError('Unexpected execution')


    error = os.system('./conda config --add channels conda-forge')

    if error != 0:
        raise TypeError('Unexpected execution')

    error = os.system('./conda install libcxx')

    if error != 0:
        raise TypeError('Unexpected execution')

    #error = os.system('conda install -c conda-forge libcxx')

    #if error != 0:
    #    raise TypeError('Unexpected execution')

    #error = os.system('./conda install -c anaconda libgcc')

#    if error != 0:
#       raise TypeError('Unexpected execution')


    #NOPE error = os.system('./conda install -c anaconda msarahan')
    #NOPE error = os.system('./conda install -c anaconda conda-forge')
    os.chdir(actual_path)
except:
    input('An error occured during installation of supplementary packages in miniconda')
    exit(1)

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
    sys.exit(1)
    
print('***** Installation of NACCESS in the conda env *****')

try:
#Copie de NACCESS Dans l'environnement

    os.chdir('./lib/NACCESS/')
    liste_fichiers_naccess = os.listdir()

    for fichier_naccess in liste_fichiers_naccess:
        print('Copying '+str(fichier_naccess)+' to conda env')
        error = os.system('cp ./'+str(fichier_naccess)+' '+str(conda_path)+'/../envs/'+str(envname)+'/bin/'+str(fichier_naccess))

        if error != 0:
            raise TypeError('Unexpected execution')


    os.chdir(current_path)
    print('\n********************************************************************************\nNACCESS has been successfully installed ! \n********************************************************************************\n')

except:
    print('An error has occured while installing naccess in conda env. Please retry')
    input('')
    sys.exit(1)

print('Saving installation directories to installout.dat')

try:
    with open('installout.dat', 'w') as filout:
        filout.write(conda_path)
except:
    print('WARNING: An error occured while saving the installation directory PATH')
    

print(' \n\n ********************************************************************************\n MEETDOCK ONE AND ALL ITS DEPENDENCIES HAVE BEEN INSTALLED SUCCESSFULLY \n********************************************************************************')

for ligne in fichier:
    print(ligne, end = '')

input('Press a key to end the installation')
