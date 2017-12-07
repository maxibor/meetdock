#!usr/env/bin python3
#DELEVOYE Guillaume & GRAVEY Francois

import logging
import os
import sys

from combine_methods import *
from TMscore_RMSD import *

os.system('rm ./appliqueur.log')
logging.basicConfig(filename='./appliqueur.log',level=logging.DEBUG, format='%(asctime)s %(message)s')    
logging.debug('Initialisation')


#def autre(rebuilt_pdb_path, receptor_chain, ligand_chain):
#    logging.debug('Applique autre methode')
#    dico_resultats = {'statpot':12, 'vdw':42, 'electro': 66, 'shape':5}
#    for cle in dico_resultats:
#        logging.debug(str(dico_resultats[cle]))
#    return dico_resultats

lib_path = os.getcwd()
print(lib_path)

def delete_hetatm(pdb_filename):
    command = "grep -v 'HETATM' {} > clean_{}".format(pdb_filename, pdb_filename)
    os.system(command)

  
def rebuild_pdb(receptor_path, ligand_path, output_path='./merged_pdb.pdb'):

    logging.debug('Merging de PDB, receptor_path = {}, ligand_path = {}, output_path = {}'.format(receptor_path, ligand_path, output_path))

    with open(output_path, 'w') as filout:
        with open(receptor_path, 'r') as recep:
            for ligne in recep:
                if ligne[0:6].strip() == 'ATOM':
                    ligne = ligne[:21] + 'A' + ligne[22:]
                    filout.write(ligne)

        filout.write('TER \n')

        with open(ligand_path, 'r') as ligand:
            for ligne in ligand:
                if ligne[0:6].strip() == 'ATOM':
                    ligne = ligne[:21] + 'B' + ligne[22:]
                    filout.write(ligne)

    if output_path != './merged_pdb.pdb':	
        logging.debug('PDB reconstruit ! Il est disponible dans ./temp/')  

def get_default_dataset(samplings_location='../data/samplings/'):
#Retourne une liste de samplings
#Les chemins des samplings sont les chemins relatifs par rapport au dossier lib !!
    origin_path = os.getcwd()
    
    logging.debug('Chargement du dataset par défaut --> get_default_dataset()')
    liste_samplings= []
    
    script_path = os.getcwd()
    logging.debug('Chemin courant: {}'.format(str(script_path)))
    logging.debug('Déplacement vers {}'.format(str(samplings_location)))
    os.chdir(samplings_location)
    logging.debug('Déplacement effectué')
    
    liste_types = os.listdir()
    logging.debug('Liste des types de sampling: {}'.format(liste_types))
    
    for sampling_type in liste_types:
    
        logging.debug('Début du parsing des noms du type {}'.format(sampling_type))
        logging.debug('Déplacement vers ' +str(sampling_type+'/sampling'))
        os.chdir(sampling_type+'/sampling')
        logging.debug('Déplacement réussi')
        
        liste_sampling_names = os.listdir()
        logging.debug('Liste des noms de sampling pour le type {}: '.format(sampling_type))
        for element in liste_sampling_names:
            logging.debug(str(element))
        
        for sampling_name in liste_sampling_names:

            sampling_dir = str(samplings_location)+str(sampling_type)+'/sampling/'+str(sampling_name)
            
            receptor_name = str(sampling_name.split('_')[0])
            
            ligand_name = str(sampling_name.split('_')[2])
            ligand_chain = str(sampling_name.split('_')[3])
            receptor_chain = str(sampling_name.split('_')[1])
            
            ligand_path = str(samplings_location)+str(sampling_type)+'/structures-natives/'+str(ligand_name)+'_'+str(ligand_chain)+'.pdb'      
            receptor_path = str(samplings_location)+str(sampling_type)+'/structures-natives/'+str(receptor_name)+'_'+str(receptor_chain)+'.pdb'   
                    
            current_sampling = Sampling(sampling_name, sampling_type, sampling_dir, ligand_path, ligand_name, ligand_chain, receptor_path, receptor_name, receptor_chain)
            
            liste_samplings.append(current_sampling)
            del(current_sampling)
        
        os.chdir(origin_path)
        logging.debug('Retour vers {}'.format(samplings_location))
        os.chdir(str(samplings_location))
        
    logging.debug('Retour au PATH initial')
    os.chdir(origin_path)        
    return liste_samplings
    
class Sampling:
    #Attributs
    sampling_name = ''; sampling_type = ''; sampling_dir = ''
    ligand_path = ''; ligand_name = ''; ligand_chain = ''
    receptor_path = ''; receptor_name = ''; receptor_chain = ''
        
    nb_conformations = None
    
    liste_resultats = []
    
    def __init__(self, sampling_name, sampling_type, sampling_dir, ligand_path, ligand_name, ligand_chain, receptor_path, receptor_name, receptor_chain):
    
        self.sampling_name = str(sampling_name); self.sampling_type = str(sampling_type)
        self.sampling_dir = str(lib_path)+'/'+str(sampling_dir); self.ligand_path = str(lib_path)+'/'+str(ligand_path)
        self.ligand_name = str(ligand_name); self.ligand_chain = str(ligand_chain)
        self.receptor_path = str(lib_path)+'/'+str(receptor_path); self.receptor_name = str(receptor_name)
        self.receptor_chain = str(receptor_chain) ; self.nb_conformations = None
        
        
    def __str__(self):        
        return 'Caractéristiques de l\'objet sampling: SAMPLING_NAME = {} \n SAMPLING_TYPE = {} \n SAMPLING_DIR = {} \n LIGAND_PATH = {} \n LIGAND_NAME = {} \n LIGAND_CHAIN = {} \n RECEPTOR_PATH = {} \n RECEPTOR_NAME = {} \n RECEPTOR_CHAIN = {}'.format(self.sampling_name, self.sampling_type, self.sampling_dir, self.ligand_path, self.ligand_name, self.ligand_chain, self.receptor_path, self.receptor_name, self.receptor_chain)
        
        
    def __eq__(self, c):
    #Ne compare pas les chemins, seulement la nature du sampling
    # c --> 'compare' (sampling to compare)
        if c.sampling_name == self.sampling_name:
            if c.sampling_type == self.sampling_type:
                if c.ligand_name == self.ligand_name:
                    if c.receptor_name == self.receptor_name:
                        if c.ligand_chain == self.ligand_chain:
                            if c.receptor_chain == self.ligand_chain:
                                return True
        else:
            return False
            
                 
class PDB_Analysis:

    pdb_name = ''
    type_sampling = ''
    valeurs = {}
    isnative = False
    
    def __init__(self, isnative = False):
        self.pdb_name = ''
        self.type_sampling = ''
        self.valeurs = {}
        self.isnative = None
        
        if isnative == True:
            self.valeurs['is_native'] = True #L'info n'est pas redondante: Cette ligne sert à écrire dans le tableau de valeurs finale
            self.isnative = True #Et cette ligne sert de flag pour que le programme puisse gérer correctement l'info sans avoir à rechercher dans le dico
        else:
            self.valeurs['is_native'] = False
            self.isnative = False
            
    #def __str__(self):
    #    ligne = ''
    #    i = 0
    #    for cle in liste_valeurs:
    #        ligne = ligne + liste_valeurs[cle]
    #        if i < len(liste_valeurs):
    #            ligne = ligne + '\t'
    #        i += 1
    #        
    #    return ligne
        
class Dataset:
    liste_samplings = []
    #Contiendra une liste de samplings
    liste_techniques = []
    #Contiendra une liste de références vers des fonctions
    liste_resultats = []
    #Contiendra une liste d'objets PDB_Analysis
    
    output_dir = ''
    temp_dir = ''
    data_dir = ''
    
    def __init__(self, liste_samplings = [], liste_techniques = [], default = 'YES'):
        if default == 'YES':
            self._init__default()
        else:
            self._init__special(liste_samplings, liste_techniques)   
           
    def _init__default(self):
        
        self.output_dir = lib_path+'/../out/'
        self.temp_dir = lib_path+'/../temp/'
        self.data_dir = lib_path+'/../data/'
        
        logging.debug('Création du dataset')
        logging.debug('Récupération des samplings')   
         
        self.liste_samplings = get_default_dataset()
        logging.debug('Noms des samplings récupérés:')
        
        for element in self.liste_samplings:
            logging.debug(str(element))     
            
        self.liste_techniques = [zang_scores_calculs, combine_score]
        
        logging.debug('Liste des techniques à appliquer sur ce dataset')
        
        for element in self.liste_techniques:
            logging.debug(str(element)) 
    
    def _init__special(self, liste_samplings, liste_techniques):
        logging.debug('Création d\'un dataset specifique : {}'.format(self.__name__))

        self.output_dir = lib_path+'/../out/'
        self.temp_dir = lib_path+'/../temp/'
        self.data_dir = lib_path+'/../data/'
        
        self.liste_samplings = liste_samplings
        self.liste_techniques = liste_techniques

        logging.debug('Noms des samplings récupérés:')
        
        for element in self.liste_samplings:
            logging.debug(str(element))     
            
        self.liste_techniques = liste_techniques
        logging.debug('Liste des techniques à appliquer sur ce dataset')
        
        for element in self.liste_techniques:
            logging.debug(str(element)) 

    def apply_methods(self):
    
        prefix = None #Pour l'enregistrement des résultats
    
        logging.debug('********APPLICATION DES METHODES EN COURS********')
        logging.debug('Application pour les structures natives: RMSD et tmscore ne seront pas effectués')
        
        #En premier lieu on s'occupe des structures natives
        
        logging.debug('APPLICATION DES TECHNIQUES POUR LES STRUCTURES NATIVES')
        for sampling in self.liste_samplings:
        #... DE chacun des samplings

            rebuilt_pdb_path = self.temp_dir+'/'+sampling.sampling_name+'_native.pdb'
            recepteurpath = sampling.receptor_path
            ligandpath = sampling.ligand_path
            
            #On reconstruit la structure native
            rebuild_pdb(receptor_path = recepteurpath, ligand_path = ligandpath, output_path = rebuilt_pdb_path)
            logging.debug('Rebuilding native from: \n\treceptor {} \n\t ligand {}'.format(recepteurpath, ligandpath))
            
            resultats_de_ce_pdb = PDB_Analysis(isnative = True)
            resultats_de_ce_pdb.pdb_name = rebuilt_pdb_path.split('/')[-1].split('.')[0]
            resultats_de_ce_pdb.type_sampling = sampling.sampling_type
            
            #On y applique les techniques demandées
            for technique in self.liste_techniques:
                dico_resultats = None
                logging.debug('On applique la technique {} au sampling {}'.format(technique,sampling.sampling_name))
                if technique != zang_scores_calculs:
                    
                    dico_resultats = technique(rebuilt_pdb_path, list(str(sampling.receptor_chain)), list(str(sampling.ligand_chain)))

                else:
                    logging.debug('Filling with NA for tmscore, rmsd and rmsd_align')
                    dico_resultats = {}
                    dico_resultats['rmsd']='NA'
                    dico_resultats['rmsd_align']='NA'
                    dico_resultats['tmscore']='NA'
                    
                for cle in dico_resultats:
                    logging.debug('Valeurs: {} , {}'.format(cle, dico_resultats[cle]))
                    resultats_de_ce_pdb.valeurs[cle]=dico_resultats[cle]
                del(dico_resultats)   
            
            #On ajoute le résultat à la liste des résultats du dataset     
            self.liste_resultats.append(resultats_de_ce_pdb)
            
            del(resultats_de_ce_pdb)
            del(rebuilt_pdb_path)
            del(recepteurpath)
            del(ligandpath)
            
        #Ensuite des structures samplées
        
        for sampling in self.liste_samplings:
            os.chdir(sampling.sampling_dir)
            #On se place dans le répertoire de sampling et on liste son contenu
            liste_pdb = os.listdir()
            
            pdb_natif_path = self.temp_dir+'/'+sampling.sampling_name+'_native.pdb'
            logging.debug('pdb_natif_path = {}'.format(str(pdb_natif_path)))
            #On repère l'emplacement de la structure native pour faire le tmscore et le rmsd
            
            for pdb in liste_pdb:
                #Sur chaque pdb on applique toutes les techniques
            
                rebuilt_pdb_path = self.temp_dir+sampling.sampling_name+pdb
                logging.debug('rebuilt_pdb_path = {}'.format(str(rebuilt_pdb_path)))
                recepteurpath = sampling.receptor_path
                ligandpath = os.getcwd()+'/'+pdb
            
                rebuild_pdb(receptor_path = recepteurpath, ligand_path = ligandpath, output_path = rebuilt_pdb_path)
                resultat_de_ce_pdb = PDB_Analysis(isnative = False)
                
                resultats_de_ce_pdb = PDB_Analysis(isnative = False)
                resultats_de_ce_pdb.pdb_name = rebuilt_pdb_path.split('/')[-1].split('.')[0]
                resultats_de_ce_pdb.type_sampling = sampling.sampling_type
                
                for technique in self.liste_techniques:
                    dico_resultats = None
                    if technique != zang_scores_calculs:
                        dico_resultats = technique(rebuilt_pdb_path,list(str(sampling.receptor_chain)),list(str(sampling.ligand_chain))) 
                                                                 
                    else:
                        dico_resultats = technique(rebuilt_pdb_path, pdb_natif_path)

                    for cle in dico_resultats:
                        logging.debug('Valeurs: {} , {}'.format(cle, dico_resultats[cle]))
                        resultats_de_ce_pdb.valeurs[cle]=dico_resultats[cle]
                    del(dico_resultats)    
                    
                self.liste_resultats.append(resultats_de_ce_pdb)
                
                del(resultats_de_ce_pdb)
                del(rebuilt_pdb_path)
                del(recepteurpath)
                del(ligandpath)
                       
            os.chdir(lib_path)
            #Retour au path de départ
            
            prefix = sampling.sampling_name
            #préfixe d'enregistrement des résultats du sampling
            
            self._write_resultats(prefix)
            #On enregistre tous les résultats du sampling et on passe au suivant !

        
    def __add__(self, autre_dataset): #Manque la fusion des résultats !
    
        fusion_techniques = self.liste_techniques  + [i for i in autre_dataset.liste_techniques if i not in self.liste_techniques]
        fusion_resultats = self.liste_resultats + [i for i in autre_dataset.liste_resultats if i not in self.liste_resultats]
        fusion_samplings = self.liste_samplings + [i for i in autre_dataset.liste_samplings if i not in self.liste_samplings]
        
        #fusion_techniques = self.liste_techniques + autre_dataset.liste_techniques
        #fusion_resultats = self.liste_resultats + autre_dataset.liste_resultats
        #fusion_samplings = self.liste_samplings + autre_dataset.liste_samplings
        
        fusion_datasets = Dataset(fusion_samplings, fusion_techniques, fusion_resultats, default = 'NO')
        return fusion_datasets
            
    def __str__(self, detailed = False):
    
        str_retour = ''
    
        if not detailed:
            chaine_retour = ['\n*****DATASET OBJECT*****\n', str(self.__class__), '\n', 'LISTE DES TECHNIQUES: \n']
            
            if len(self.liste_techniques) < 1:
                chaine_retour.append('\t (Aucune technique)\n')
            else:
                for technique in self.liste_techniques:
                    chaine_retour.append('\t-Technique utilisée: '+str(technique)+'\n')

            chaine_retour.append('LISTE DES RESULTATS :\n')
            
            if len(self.liste_resultats) < 1:
                chaine_retour.append('\t (Aucun résultat) \n')
            else:
                for resultat in self.liste_resultats:
                    chaine_retour.append(str(resultat)+'\n')

            #chaine_retour.append('LISTE DES SAMPLINGS :')
            #for sampling in self.liste_samplings:
            #    chaine_retour.append(str(sampling)+'\n*********\n')
            
            chaine_retour.append('LISTE DES SAMPLINGS :\n')
            
            if len(self.liste_samplings) < 1:
                chaine_retour.append('\t'+'(Aucun sampling)')
            else:
                for sampling in self.liste_samplings:
                    chaine_retour.append('\t'+str(sampling.sampling_name)+' '+sampling.__repr__()+'\n')
                 
            
            for element in chaine_retour:
                str_retour = str_retour + element

            return(str(str_retour))    
        else:
            #To Implement
            pass
                
    def _write_resultats(self,prefix):
        fichier = open(str(self.output_dir+prefix+'_resultats.out'), 'w')
        
        liste = 'PDB_name'+'\t'+'Type_sampling'+'\t'+'IsNative'+'\t'+'statpot'+'\t'+'vdw'+'\t'+'electro'+'\t'+'shape'+'\t'+'rmsd' +'\t'+'rmsd_align'+'\t'+'tmscore'
        fichier.write(liste)
        fichier.write('\n')
        del(liste)
        
        for resultat in self.liste_resultats:
            chaine = str(resultat.pdb_name + '\t' + str(resultat.type_sampling) + '\t' + str(resultat.isnative) + '\t' + str(resultat.valeurs['statpot']) + '\t' + str(resultat.valeurs['vdw']) + '\t' + str(resultat.valeurs['electro']) + '\t'+ str(resultat.valeurs['shape']) + '\t' + str(resultat.valeurs['rmsd']) + '\t' + str(resultat.valeurs['rmsd_align']) + '\t' + str(resultat.valeurs['tmscore']) + '\t')
            

            fichier.write(chaine)
            fichier.write('\n')
                
        fichier.close()    
        
    def _clean_temps(self):
        pass
        #To implement

            
if __name__ == '__main__':
    print('Please check the log: tail -f ./Appliqueur.log\n')
    my_data = Dataset()
    print('Dataset is loaded')
    my_data.apply_methods()
    print('DONE')
