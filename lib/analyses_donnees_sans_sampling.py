#!/usr/bin/env python3
import sys
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils import check_array
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from scipy import sparse
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import pickle


class CategoricalEncoder(BaseEstimator, TransformerMixin):
    """Encode categorical features as a numeric array.
    The input to this transformer should be a matrix of integers or strings,
    denoting the values taken on by categorical (discrete) features.
    The features can be encoded using a one-hot aka one-of-K scheme
    (``encoding='onehot'``, the default) or converted to ordinal integers
    (``encoding='ordinal'``).
    This encoding is needed for feeding categorical data to many scikit-learn
    estimators, notably linear models and SVMs with the standard kernels.
    Read more in the :ref:`User Guide <preprocessing_categorical_features>`.
    Parameters
    ----------
    encoding : str, 'onehot', 'onehot-dense' or 'ordinal'
        The type of encoding to use (default is 'onehot'):
        - 'onehot': encode the features using a one-hot aka one-of-K scheme
          (or also called 'dummy' encoding). This creates a binary column for
          each category and returns a sparse matrix.
        - 'onehot-dense': the same as 'onehot' but returns a dense array
          instead of a sparse matrix.
        - 'ordinal': encode the features as ordinal integers. This results in
          a single column of integers (0 to n_categories - 1) per feature.
    categories : 'auto' or a list of lists/arrays of values.
        Categories (unique values) per feature:
        - 'auto' : Determine categories automatically from the training data.
        - list : ``categories[i]`` holds the categories expected in the ith
          column. The passed categories are sorted before encoding the data
          (used categories can be found in the ``categories_`` attribute).
    dtype : number type, default np.float64
        Desired dtype of output.
    handle_unknown : 'error' (default) or 'ignore'
        Whether to raise an error or ignore if a unknown categorical feature is
        present during transform (default is to raise). When this is parameter
        is set to 'ignore' and an unknown category is encountered during
        transform, the resulting one-hot encoded columns for this feature
        will be all zeros.
        Ignoring unknown categories is not supported for
        ``encoding='ordinal'``.
    Attributes
    ----------
    categories_ : list of arrays
        The categories of each feature determined during fitting. When
        categories were specified manually, this holds the sorted categories
        (in order corresponding with output of `transform`).
    Examples
    --------
    Given a dataset with three features and two samples, we let the encoder
    find the maximum value per feature and transform the data to a binary
    one-hot encoding.
    >>> from sklearn.preprocessing import CategoricalEncoder
    >>> enc = CategoricalEncoder(handle_unknown='ignore')
    >>> enc.fit([[0, 0, 3], [1, 1, 0], [0, 2, 1], [1, 0, 2]])
    ... # doctest: +ELLIPSIS
    CategoricalEncoder(categories='auto', dtype=<... 'numpy.float64'>,
              encoding='onehot', handle_unknown='ignore')
    >>> enc.transform([[0, 1, 1], [1, 0, 4]]).toarray()
    array([[ 1.,  0.,  0.,  1.,  0.,  0.,  1.,  0.,  0.],
           [ 0.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.]])
    See also
    --------
    sklearn.preprocessing.OneHotEncoder : performs a one-hot encoding of
      integer ordinal features. The ``OneHotEncoder assumes`` that input
      features take on values in the range ``[0, max(feature)]`` instead of
      using the unique values.
    sklearn.feature_extraction.DictVectorizer : performs a one-hot encoding of
      dictionary items (also handles string-valued features).
    sklearn.feature_extraction.FeatureHasher : performs an approximate one-hot
      encoding of dictionary items or strings.
    """

    def __init__(self, encoding='onehot', categories='auto', dtype=np.float64,
                 handle_unknown='error'):
        self.encoding = encoding
        self.categories = categories
        self.dtype = dtype
        self.handle_unknown = handle_unknown

    def fit(self, X, y=None):
        """Fit the CategoricalEncoder to X.
        Parameters
        ----------
        X : array-like, shape [n_samples, n_feature]
            The data to determine the categories of each feature.
        Returns
        -------
        self
        """

        if self.encoding not in ['onehot', 'onehot-dense', 'ordinal']:
            template = ("encoding should be either 'onehot', 'onehot-dense' "
                        "or 'ordinal', got %s")
            raise ValueError(template % self.handle_unknown)

        if self.handle_unknown not in ['error', 'ignore']:
            template = ("handle_unknown should be either 'error' or "
                        "'ignore', got %s")
            raise ValueError(template % self.handle_unknown)

        if self.encoding == 'ordinal' and self.handle_unknown == 'ignore':
            raise ValueError("handle_unknown='ignore' is not supported for"
                             " encoding='ordinal'")

        X = check_array(X, dtype=np.object, accept_sparse='csc', copy=True)
        n_samples, n_features = X.shape

        self._label_encoders_ = [LabelEncoder() for _ in range(n_features)]

        for i in range(n_features):
            le = self._label_encoders_[i]
            Xi = X[:, i]
            if self.categories == 'auto':
                le.fit(Xi)
            else:
                valid_mask = np.in1d(Xi, self.categories[i])
                if not np.all(valid_mask):
                    if self.handle_unknown == 'error':
                        diff = np.unique(Xi[~valid_mask])
                        msg = ("Found unknown categories {0} in column {1}"
                               " during fit".format(diff, i))
                        raise ValueError(msg)
                le.classes_ = np.array(np.sort(self.categories[i]))

        self.categories_ = [le.classes_ for le in self._label_encoders_]

        return self

    def transform(self, X):
        """Transform X using one-hot encoding.
        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The data to encode.
        Returns
        -------
        X_out : sparse matrix or a 2-d array
            Transformed input.
        """
        X = check_array(X, accept_sparse='csc', dtype=np.object, copy=True)
        n_samples, n_features = X.shape
        X_int = np.zeros_like(X, dtype=np.int)
        X_mask = np.ones_like(X, dtype=np.bool)

        for i in range(n_features):
            valid_mask = np.in1d(X[:, i], self.categories_[i])

            if not np.all(valid_mask):
                if self.handle_unknown == 'error':
                    diff = np.unique(X[~valid_mask, i])
                    msg = ("Found unknown categories {0} in column {1}"
                           " during transform".format(diff, i))
                    raise ValueError(msg)
                else:
                    # Set the problematic rows to an acceptable value and
                    # continue `The rows are marked `X_mask` and will be
                    # removed later.
                    X_mask[:, i] = valid_mask
                    X[:, i][~valid_mask] = self.categories_[i][0]
            X_int[:, i] = self._label_encoders_[i].transform(X[:, i])

        if self.encoding == 'ordinal':
            return X_int.astype(self.dtype, copy=False)

        mask = X_mask.ravel()
        n_values = [cats.shape[0] for cats in self.categories_]
        n_values = np.array([0] + n_values)
        indices = np.cumsum(n_values)

        column_indices = (X_int + indices[:-1]).ravel()[mask]
        row_indices = np.repeat(np.arange(n_samples, dtype=np.int32),
                                n_features)[mask]
        data = np.ones(n_samples * n_features)[mask]

        out = sparse.csc_matrix((data, (row_indices, column_indices)),
                                shape=(n_samples, indices[-1]),
                                dtype=self.dtype).tocsr()
        if self.encoding == 'onehot-dense':
            return out.toarray()
        else:
            return out

class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[self.attribute_names].values
    
def crea_tableau(fichier):
    """Fonction qui transforme un fichier au format .csv en un DataFrame pandas
    Input : fichier.csv
    Output : Pandas DataFrame
    """
    df = pd.io.parsers.read_csv('{}'.format(fichier), index_col=False, sep=';')
    return df

def modif_data(fichier):
    """Fonction qui élimine du DataFrame pandas toutes les valeurs parasites:
    les colones qui ne contiennent que des zéros, les lignes qui correspondent aux
    structures natives et tous les complexes pour lesquels une des valeurs est
    abérente, dans le cas considéré, zéro
    Input : Pandas DataFrame
    Output : Pandas DataFrame
    """
    data = crea_tableau(fichier)
    data = data.drop(['pdb'], axis =1)
    #data = data[data.statpot != 0]
    data = data[data.vdw != 0]
    data = data.rename(columns = {'shape':'shape_int'})
    data = data[data.shape_int !=0]
    data = data.reset_index(drop=True)
    return data

def data_num(fichier, liste):
    """Fonction qui permet de ne garder que les paramètres qui doivent être normalisés
    Input : fichier au format csv et une liste qui contient les paramètres qui ne 
    doivent pas être conservés
    Output : Pandas DataFrame
    """
    data = modif_data(fichier)
    for parametre in liste:
        data = data.drop(parametre, axis = 1)
    return data

def miss_values(fichier, liste):
    """Fonction qui élimine toute donnée NUMERIQUE manquante dans le Pandas 
    DataFrame. NECESSITE D'ELIMINER TOUTE COLONE CONTENANT DU TEXTE !!!!!!
    Les données manquantes sont remplacées par la médiane de la colone dans 
    laquelle se trouve les données manquante
    Input : DataFrame
    Output : DataFrame sans aucune donnée numérique manquante
    """
    dataframe = data_num(fichier, liste)
    imputer = Imputer(strategy = 'median')
    imputer.fit(dataframe)
    x = imputer.transform(dataframe)
    data_tr = pd.DataFrame(x, columns = dataframe.columns)
    return data_tr

def min_max_scale(fichier, liste):
    """Fonction qui transforme les données numériques contenues dans le pandas
    DataFrame par des valeurs contenues entre 0 et 1 via l'utilisation de la fonction
    min_max_scaler de sklearn
    Input : fichier.csv et liste des parametres A NE PAS MODIFIER
    Output : Pandas DataFrame
    """
    dataframe = miss_values(fichier, liste)
    x = dataframe.values
    min_max_scaler = MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    pdf = pd.DataFrame(x_scaled, columns = dataframe.columns.values)
    return pdf

def stand(fichier, liste):
    """Fonction qui transforme les données numériques contenues dans le pandas
    DataFrame par des valeurs contenues entre 0 et 1 via l'utilisation de la fonction
    standardscaler de sklearn
    Input : fichier.csv et liste des parametres A NE PAS MODIFIER
    Output : Pandas DataFrame
    """
    donnees = data_num(fichier, liste)
    Y = donnees.values
    scaler = StandardScaler()
    new_data = scaler.fit_transform(Y)
    tab = pd.DataFrame(new_data, columns = donnees.columns.values)
    return tab
   
def correl(parametre, donnees):
    """Fonction qui recherche dans un DataFrame les valeurs de corrélations 
    linéaires entre le paramètre d'input et les autres valeurs contenues dans le
    DataFrame.
    Inputs : Paramètre pour lequel on recherche la correlation, DataFrame
    Outputs : Valeurs des corrélations linéaires entre les différentes valeures
    """
    corr_matrix = donnees.corr()
    return corr_matrix[parametre].sort_values(ascending=False)
    
def convertion(fichier,parametre):
    """Fonction qui transforme les données de type alphabet en données numériques
    Input : fichier.csv, parametre qui doit être converti
    Output : numppy score matice
    """
    data = modif_data(fichier)
    text = data[parametre]
    text_cat_encoded, sampling_categories = text.factorize()
    encoder = OneHotEncoder()
    text_cat_1hot = encoder.fit_transform(text_cat_encoded.reshape(-1,1))
    return text_cat_1hot

def regroup(fichier, liste):
    """Fonction qui regroupe toutes les données, les données brutes, les données
    modifiées par la méthode de min_max_scaler et de normalisation de Sklearn
    Input : fichier.csv et une liste de parametres non numérique et qui ne doivent 
    pas être 'normalisés'
    Output : Pandas DataFrame
    """
    raw = modif_data(fichier)
    min_max = min_max_scale(fichier, liste)
    norm = stand(fichier, liste)    
    colonnes = []
    colonnes_2 = []
    for nom in min_max.columns.values:
        nom = str(nom) + '_min_max'
        colonnes.append(nom)
    min_max_data = pd.DataFrame(min_max.values, columns = colonnes)
    for nom in norm.columns.values:
        nom = str(nom) + '_norm'
        colonnes_2.append(nom)
    norm_data = pd.DataFrame(norm.values, columns = colonnes_2)
    frames = [raw, min_max_data, norm_data]
    all = pd.concat(frames, axis =1)
    return all


def display_scores(scores):
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("Standard deviation:", scores.std())


################################################
####Programme principal#########################
################################################
#fichier = input('Entrez le nom du fichier à analyser : ')
fichier = 'enzyme_ligand_result.csv'
liste = ['tm_score']
donnees = modif_data(fichier)
#print(donnees)

#Selection parmi les données, de celles qui vont servir à l'apprentissage = train_set
train_set, test_set = train_test_split(donnees, test_size=0.2, random_state=1)
    
#On exclu des modifications prochaines le label contenu dans le fichier.csv
score = train_set.drop('tm_score', axis =1)
    
#On définit ce qui est numérique et ce qui ne l'est pas, numérique = score_num
#puis on créé une liste, num_attribs
#ce qui n'est pas numérique est désigné sous le nom de cat_attribs
score_num = score
num_attribs = list(score_num)
    
#Création d'un pipeline de modifications des données numérique, ici:
#remplacement des données manquantes par la médiane
#puis standardisation des données/normalisation par StandardScaler
num_pipeline = Pipeline([('selector', DataFrameSelector(num_attribs)),\
('imputer', Imputer(strategy="median")),('std_scaler', StandardScaler())])


score_prepared = num_pipeline.fit_transform(score_num)
    
#Sortie
score_prepared
score_label = train_set['tm_score']


################################################################################
########## PREMIER MODEL REGRESSION LINEAIRE ###################################
################################################################################

lin_reg = LinearRegression()
lin_reg.fit(score_prepared, score_label)

some_data = score.iloc[:5]
some_labels = score_label.iloc[:5]
some_data_prepared = num_pipeline.fit_transform(some_data)
#print('Predictions:', lin_reg.predict(some_data_prepared))
#print("Labels:", list(some_labels))


#Evaluation des performances
tm_prediction = lin_reg.predict(score_prepared)
lin_mse = mean_squared_error(score_label, tm_prediction)
lin_rmse = np.sqrt(lin_mse)
#print(lin_rmse)

################################################################################
########## DEUXIEME MODEL DecisionTreeRegressor ################################
################################################################################

tree_reg = DecisionTreeRegressor()
tree_reg.fit(score_prepared, score_label)

#Evaluation des performances
tm_tree_prediction = tree_reg.predict(score_prepared)
mse_tree = mean_squared_error(score_label, tm_tree_prediction)
rmse_tree = np.sqrt(mse_tree)
#print(rmse_tree)

################################################################################
########## TROISIEME MODEL RANDOM FOREST REGRESSOR #############################
################################################################################

forest_reg = RandomForestRegressor()
forest_reg.fit(score_prepared, score_label)

tm_forest_prediction = forest_reg.predict(score_prepared)
mse_forest = mean_squared_error(score_label, tm_forest_prediction)
rmse_forest = np.sqrt(mse_forest)
#print(rmse_forest)


################################################################################
########## ANALYSE DES PERFORMANCES EN RANDOMINSANT LES TRAINS SET #############
################################################################################

#utilisation de la variable cvs pour référer à cross_val_score
cvs_tree = cross_val_score(tree_reg, score_prepared, score_label, scoring="neg_mean_squared_error", cv=100)
tree_rmse_scores = np.sqrt(-cvs_tree)
print('Model Tree')
display_scores(tree_rmse_scores)
#print('\n')

cvs_linear = cross_val_score(lin_reg, score_prepared, score_label, scoring="neg_mean_squared_error", cv=100)
lin_rmse_scores = np.sqrt(-cvs_linear)
print('Model lineaire')
display_scores(lin_rmse_scores)
#print('\n')

cvs_forest = cross_val_score(forest_reg, score_prepared, score_label, scoring="neg_mean_squared_error", cv=100)
forest_rmse_scores = np.sqrt(-cvs_forest)
print('Model random forest')
display_scores(forest_rmse_scores)
#print('\n')

################################################################################
########## ANALYSE DES MEILLEURS PARAMETRES ####################################
################################################################################


param_grid = [{'n_estimators':[10,50, 100], 'max_features':[1,2,3,4]},\
{'bootstrap':[True], 'n_estimators':[10,50, 100], 'max_features':[1,2,3,4]}]

grid_search = GridSearchCV(forest_reg, param_grid, cv=10, scoring = "neg_mean_squared_error")

grid_search.fit(score_prepared, score_label)

print(grid_search.best_params_)
print(grid_search.best_estimator_)

cvres = grid_search.cv_results_
for mean_score, params in zip(cvres['mean_test_score'], cvres['params']):
    print(np.sqrt(-mean_score), params)

################################################################################
########## Utilisation des données de test #####################################
################################################################################
final_model = grid_search.best_estimator_
print(final_model.feature_importances_)


#Préparation des données
X_test = test_set.drop('tm_score', axis=1)
Y_test = test_set['tm_score'].copy()
X_test_prepared = num_pipeline.transform(X_test)

final_prediction = final_model.predict(X_test_prepared)

final_mse = mean_squared_error(Y_test, final_prediction)
print('Mean squared error des donnees de test')
print(np.sqrt(final_mse))

#Ce qu'il reste à faire: est ce possible dans une fonction ?
#Comment stocker le model ?
#doit on utiliser le type de sampling ?
#doit on diviser le statpot par la longueur du pdb ?



#A = final.sort_values(by=['tm_score_predit'], ascending = False)

#A.iloc[:11].to_csv('final.csv', sep= ';', decimal = ',')


pickle_out = open('learning.pickle', 'wb')
pickle.dump(final_model, pickle_out)
pickle_out.close()

pickle_out = open('data.pickle', 'wb')
pickle.dump(X_test, pickle_out)
pickle_out.close()
