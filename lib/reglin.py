
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df = pd.io.parsers.read_csv('1j5p_A_1j5p_B_resultats.csv', index_col=False, sep='\t')
df = df.dropna(axis=0, how='any')
print(df)
X = df.drop(columns=['PDB_name', 'Type_sampling', 'IsNative', 'rmsd', 'rmsd_align', 'tmscore'])
y = df[['tmscore']]
#print(X)
#print(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)
regression_model = LinearRegression()
regression_model.fit(X_train, y_train)

for idx, col_name in enumerate(X_train.columns):
    print("The coefficient for {} is {}".format(col_name, regression_model.coef_[0][idx]))
intercept = regression_model.intercept_[0]

print("The intercept for our model is {}".format(intercept))
print(regression_model.score(X_test, y_test))

