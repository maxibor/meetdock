#!usr/env/bin python3
#DELEVOYE Guillaume
#15/11/17

#Objects and functions to handle the sampling datasets and using various methods on them

#####NON FONCTIONNEL POUR L'INSTANT
#####NECESSITE D'ETRE CORRECTEMENT PLACE DANS LA BONNE ARBORESCENCE POUR FONCTIONNER
#####NE PAS HESITER A ME DEMANDER

#**********************************************************#

import os
import logging
#import parsing #A modifier en concertation avec francois pour inclure à l'avenir les parseurs

logging.basicConfig(filename='datahandler.log',level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.debug('Datahandler loading...')

#import script_francois # --> Pas encore au format de fonction pour l'instant
    # --> Needed to have so that we can use both methods that need splitted .pdb for ligand and receptor and methods that need a unified .pdb of the whole complexe

'''Classes and functions to handle easily the sampling datasets and apply methods on them'''

#**********************************************************#


class DataHandlerObject:
    #Not needed now
    '''Basic object from which every other object of the library heritates'''
    number_handler = 0
    def __init__ (self):
        DataHandlerObject.number_handler += 1
        logging.debug('One DataHandlerObject created, total created = '+str(number_handler))
        
#**********************************************************#

def get_default_samplings():

    logging.debug("Beginning to get the default samplings")
    samplings = []
    
    base_path = os.getcwd()
    
    logging.debug("Current directory is setted to"+str(base_path))
    logging.debug("Moving to default Data Directory")
    
    try:
        os.chdir('./Data')
        logging.debug("Moved successfully to Data directory")
    except:
        logging.critical("Failed to move to default data directory ! Fatal error")
        exit(-1)
    
    logging.debug("Listing the different types of samplings")
    
    try:
        list_types_sampling = os.listdir()
        logging.debug("Listing of sampling types succeeded: Here is the list")
        logging.debug(str(list_types_sampling))
        logging.debug('There are '+str(len(list_types_sampling))+' sampling types in the default folder')
        logging.debug("PLease check that this list is correct ! Every repository has been accounted")
    except:
        logging.critical("Could not list the directories. Process failed. Exit, returning -1")
        exit(-1)
        
    for type_sampling in list_types_sampling:

        logging.debug("Moving to default sampling directory of type "+ str(type_sampling))
        try:
            os.chdir('./'+str(type_sampling)+"/sampling/")
            logging.debug('... Moved sucessfully to sampling directory')
        except:
            logging.error('An error occured during opening of the sampling directory')
            
        logging.debug('Trying to list the files in the sampling directory')
        
        try:        
            liste_noms = os.listdir()
            logging.debug('Listing --> sucessfull')
            logging.debug('Here is how the list of samplings is looking:')
            
            for i in range (0,11,1): #Printing the first part of the list
                try:
                    logging.debug('... 'str(liste_noms[i]))
                    if i == 10:
                        logging.debug('... etc')
                except IndexError:
                    if i != 0:
                        pass
                    else:
                        logging.error("An error occured while trying to examinate the list of samplings")
                        
            logging.debug("The list of sampling files in this directory is "+str(len(liste_noms)))
            
            if len(liste_noms) >= 5000:
                logging.warning('ATTENTION: Il y a plus de 5000 fichiers dans ce répertoire ! Peut causer des soucis de commandes bash')            
        except:
            system.error('Une erreur est suvenue pendant le listing')    

        system.logging('Récupération

        for nom in liste_noms:
            #Partant du principe que le nom est au format [recepteur]_[chaine_rec]_[ligand]_[chaine_ligand]_[No]

            sampling = {} 
            
            sampling['sampling_path']= './Data/'+str(type_sampling)+"/sampling/"+str(name_sampling)
            sampling['receptor_path'] = './Data/'+str(type_sampling)+"/structures_natives"
            sampling['ligand_path'] = './Data/'+str(type_sampling)+"/structures_natives"
        
            sampling['receptor_chain'] = nom.split("_")[1]
            sampling['ligand_chain'] = nom.split("_")[3]
        
            sampling['receptor_name'] = nom.split("_")[0]
            sampling['ligand_name'] = nom.split("_")[2]
            
            sampling['sampling_type'] = str(type_sampling)
            sampling['sampling_name'] = str(nom)

            samplings.append(sampling)
            del sampling
            logging.debug('Initializing the sampling '+str(nom))

        os.chdir('../../')
        
    os.chdir(base_path)
    
    return samplings
        
def default_fft():
    logging.debug("...Applying default FFT")
    logging.debug("FFT done")
    
def default_rmsd():
    logging.debug("...Applying default RMSD")
    logging.debug("RMSD done")

def default_foldx():
    logging.debug("...Applying default foldx")
    logging.debug("foldx done")        
            
#**********************************************************#           

class Dataset(DataHandlerObject):
    ''' Class to manipulate sampling results'''
    
    sampling_list = None
    methods_list = []
    output_directory = ""
        #Must be a correct UNIX Path to store the results of the analysis
    temp_rep = ""
        #Same, but for storing the intermediate files
    resultats = None 
    
    def __init__(self, DataPath = "DEFAULT", methods_lists = "DEFAULT", sampling_list ="DEFAULT", outputref='DEFAULT', temp_list='DEFAULT', List_methods='DEFAULT', Translator = None, clean_temp = True, clean_resultats = True):
    #For now only default behaviour is implemented
        if DataPath == "DEFAULT" and sampling_list == "DEFAULT" and outputref == 'DEFAULT' and temp_list == 'DEFAULT' and List_methods == 'DEFAULT' and Translator == None and clean_temp == True and clean_resultats == True:
        
            logging.debug("Creating a default dataset")
        
            try:
                self.sampling_list = get_default_samplings()
                self.output_diretory = './output/'
                self.temp_rep = './temp'
                logging.debug('Getting default samplings succeeded, as follows:')
                
                for sampling in self.sampling_list:
                    for attrib in self.sapling_list[str(sampling)]:
                        logging.debug(str(attrib))
                
                logging.debug('Methods are loaded for default usage, as follow:')        
                self.methods_list = [default_fft, default_rmsd, default_foldx]
                for elt in self.methods_list:
                    logging.debug(elt)
                    
            except:
                logging.error('Couldn\'t get the default samplings')
            
                                           
        else:
            logging.critical('Getting other samplings than default hasn\'t been implemented yet')
            print('Getting other samplings than default ones hasn\'t been implemented yet')

    def apply_default_methods(self):
        for elt in self.methods_list:
            logging.debug('Calling the function '+str(elt))
            elt()
            
 
#**********************************************************#

if __name__ == '__main__':

    #Pour le comportement par défaut ces trois lignes suffisent
    
    my_data = Dataset()
    my_data.apply_default_methods()
    print("Over")
    input("Appuyez sur une touche pour continuer")
    
    
    
    
    
    
    
    
        
