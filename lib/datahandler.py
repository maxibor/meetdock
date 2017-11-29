#!usr/env/bin python3
#DELEVOYE Guillaume

import logging
import os

logging.basicConfig(filename='appliqueur.log',level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.debug('Initialisation')

def fft(sampling):
    resultat = 'test_fft'
    origin_path = os.getcwd()
    
    os.chdir(sampling.sampling_dir)
    liste_pdb_names = os.listdir()
    
    for pdb in liste_pdb_names:
        logging.debug("...Applying FFT to {}".format(str(pdb)))
        #Calculer la FFT pour ce pdb
        #L'écrire dans l'outputdir du sampling
    
    os.chdir(origin_path) #On se replace où on était
    logging.debug("FFT done")
    
    return resultat
    
def rmsd(sampling):
    resultat = 'test_rmsd'
    origin_path = os.getcwd()
    
    os.chdir(sampling.sampling_dir)
    liste_pdb_names = os.listdir()
    
    for pdb in liste_pdb_names:
        logging.debug("...Applying rmsd to {}".format(str(pdb)))
        #Calculer le rmsd par rapport au natif pour ce pdb
        #L'écrire dans l'outputdir du sampling
    
    os.chdir(origin_path) #On se replace où on était
    logging.debug("FFT done")
    
    return resultat

def foldx(sampling):
    resultat = 'test_foldx'
    origin_path = os.getcwd()
    
    os.chdir(sampling.sampling_dir)
    liste_pdb_names = os.listdir()
    
    for pdb in liste_pdb_names:
        logging.debug("...Applying foldx to {}".format(str(pdb)))
        #Calculer le score foldx pour ce pdb
        #L'écrire dans l'outputdir du sampling
    
    os.chdir(origin_path) #On se replace où on était
    logging.debug("FFT done")
    
    return resultat
    
def tmscore(sampling):
    resultat = 'test_TMscore'
    origin_path = os.getcwd()
    
    os.chdir(sampling.sampling_dir)
    liste_pdb_names = os.listdir()
    
    for pdb in liste_pdb_names:
        logging.debug("...Applying TM_score to {}".format(str(pdb)))
        #Calculer le TM_score pour ce pdb
        #L'écrire dans l'outputdir du sampling
    
    os.chdir(origin_path) #On se replace où on était
    logging.debug("FFT done")
    
    return resultat
    
class Sampling:
    #Attributs
    sampling_name = ''
    sampling_type = ''
    sampling_dir = ''
    
    output_dir = ''
    
    ligand_path = ''
    ligand_name = ''
    ligand_chain = ''
    
    receptor_path = ''    
    receptor_name = ''
    receptor_chain = ''
        
    nb_conformations = None
    
    def __init__(self, sampling_name, sampling_type, output_dir, sampling_dir, ligand_path, ligand_name, ligand_chain, receptor_path, receptor_name, receptor_chain):
    
        self.sampling_name = str(sampling_name)
        self.sampling_type = str(sampling_type)
        self.sampling_dir = str(sampling_dir)
        self.output_dir = str(output_dir)
        self.ligand_path = str(ligand_path)
        self.ligand_name = str(ligand_name)
        self.ligand_chain = str(ligand_chain)
        self.receptor_path = str(receptor_path)
        self.receptor_name = str(receptor_name)
        self.receptor_chain = str(receptor_chain)
        self.nb_conformations = None
        
    def __str__(self):        
        return 'Caractéristiques de l\'objet sampling: SAMPLING_NAME = {} \n SAMPLING_TYPE = {} \n OUTPUT_DIR = {} \n SAMPLING_DIR = {} \n LIGAND_PATH = {} \n LIGAND_NAME = {} \n LIGAND_CHAIN = {} \n RECEPTOR_PATH = {} \n RECEPTOR_NAME = {} \n RECEPTOR_CHAIN = {}'.format(self.sampling_name, self.sampling_type, self.output_dir, self.sampling_dir, self.ligand_path, self.ligand_name, self.ligand_chain, self.receptor_path, self.receptor_name, self.receptor_chain)
        
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
            
        
            
def get_default_dataset():
#Retourne une liste de samplings
#Les chemins des samplings sont les chemins relatifs par rapport au dossier lib !!
    origin_path = os.getcwd()
    
    logging.debug('Chargement du dataset par défaut --> get_default_dataset()')
    liste_samplings= []
    
    script_path = os.getcwd()
    logging.debug('Chemin courant: {}'.format(str(script_path)))
    logging.debug('Déplacement vers ../data')
    os.chdir('../data')
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
            
            output_dir = '../data/'+str(sampling_type)+'/output'
            sampling_dir = '../data/'+str(sampling_type)+'/sampling/'+str(sampling_name)
            
            receptor_name = str(sampling_name.split('_')[0])
            
            ligand_name = str(sampling_name.split('_')[2])
            ligand_chain = str(sampling_name.split('_')[3])
            receptor_chain = str(sampling_name.split('_')[1])
            
            ligand_path = '../data/'+str(sampling_type)+'/structures-natives/'+str(ligand_name)+'_'+str(ligand_chain)+'.pdb'      
            receptor_path = '../data/'+str(sampling_type)+'/structures-natives/'+str(receptor_name)+'_'+str(ligand_chain)+'.pdb' 
            
            logging.debug('Caractéristiques de l\'objet sampling: SAMPLING_NAME = {} \n SAMPLING_TYPE = {} \n OUTPUT_DIR = {} \n SAMPLING_DIR = {} \n LIGAND_PATH = {} \n LIGAND_NAME = {} \n LIGAND_CHAIN = {} \n RECEPTOR_PATH = {} \n RECEPTOR_NAME = {} \n RECEPTOR_CHAIN = {}'.format(sampling_name, sampling_type, output_dir, sampling_dir, ligand_path, ligand_name, ligand_chain, receptor_path, receptor_name, receptor_chain))        
                    
            current_sampling = Sampling(sampling_name, sampling_type, output_dir, sampling_dir, ligand_path, ligand_name, ligand_chain, receptor_path, receptor_name, receptor_chain)
            
            liste_samplings.append(current_sampling)
            del(current_sampling)
        
        os.chdir(origin_path)
        logging.debug('Retour vers ../data')
        os.chdir('../data')
        
    logging.debug('Retour au PATH initial')
    os.chdir(origin_path)        
    return liste_samplings        
        

class Dataset:
    liste_samplings = None
    #Contiendra une liste de samplings
    liste_techniques = None
    liste_resultats = []
    
    def __init__(self, liste_samplings = [], liste_techniques = [foldx, fft, rmsd, tmscore], liste_resultats = [], default = 'YES'):
        if default == 'YES':
            self._init__default()
        else:
            self._init__special(liste_samplings, liste_techniques, liste_resultats)   
           
    def _init__default(self):
        logging.debug('Création du dataset')
        logging.debug('Récupération des samplings')   
         
        self.liste_samplings = get_default_dataset()
        logging.debug('Noms des samplings récupérés:')
        
        for element in self.liste_samplings:
            logging.debug(str(element))     
            
        self.liste_techniques = [fft, rmsd, foldx, tmscore]
        logging.debug('Liste des techniques à appliquer sur ce dataset')
        
        for element in self.liste_techniques:
            logging.debug(str(element))
    
    def _init__special(self, liste_samplings, liste_techniques, liste_resultats):
        logging.debug('Création d\'un dataset special')
        
        self.liste_samplings = liste_samplings
        self.liste_techniques = liste_techniques
        self.liste_resultats = liste_resultats
    
            
    def apply_default_techniques(self):
    #Applique une méthode sur chaque sampling
        logging.debug('Application des techniques par défaut')
        for sampling in self.liste_samplings:
            for technique in self.liste_techniques:
                logging.debug('Application de la technique '+str(technique))
                resultat = technique(sampling)
                logging.debug('Résultat de la technique '+str(technique)+' = '+str(resultat))
                #On appelle les méthodes une à une qui sont dans self.liste_techniques
                self.liste_resultats.append(resultat)
                
        return(self.liste_resultats)
        
    def __add__(self, autre_dataset):
    
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
            
if __name__ == '__main__':
    print('Création du dataset par défaut. Checkez \"appliqueur.log\" pour le débug')
    my_data = Dataset()
    
    input('Appuyez sur entrée pour voir votre dataset')
    print(my_data)
    my_data2 = Dataset()
    #print(my_data2)
    input('my_data2 est crée, Appuyez sur entrée (My_data2 ne sera pas affiché')
    
    fusion = my_data + my_data2
    input('Voici la fusion (appuez sur entrée pour la voir)')
    print(fusion)
    
    input('Appuyez sur entrée pour voir les résultats')
    resultats = fusion.apply_default_techniques()
    print(resultats)                
         
