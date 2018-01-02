#REmoves traces of previous works
import os

os.chdir('global_out')
os.system('rm -rf *')
os.chdir('../')
os.chdir('pdb_mini')
os.system('rm -rf *')
os.chdir('../')
os.chdir('Proteins')
os.system('rm -rf *')
os.chdir('../')
