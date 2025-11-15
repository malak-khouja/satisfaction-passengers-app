# Importation des bibliothèques nécessaires
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import joblib

# Chargement des données
df = pd.read_csv("C:/Users/MALAK/OneDrive/Bureau/satisfaction-app/backend/data/train.csv")

# Nettoyage des données
threshold = len(df)*0.05
cols_to_drop = df.columns[df.isna().sum()<=threshold]
df.dropna(subset=cols_to_drop, inplace=True)
    
# Encodage des variables catégorielles importantes
dummies = pd.get_dummies(df[["satisfaction","Customer Type",'Type of Travel','Class']]).astype(int)
df = pd.concat([df,dummies],axis=1)

# Suppression des colonnes inutiles ou redondantes
df = df.drop(['Unnamed: 0','Arrival Delay in Minutes', 'Departure Delay in Minutes', 'id', "Gender", "Customer Type", 'Type of Travel', 'Class',"satisfaction","Type of Travel_Personal Travel","Customer Type_disloyal Customer","satisfaction_neutral or dissatisfied"],axis=1)

# Standardisation des variables numériques continues
scaler = StandardScaler()
df[['Age', 'Flight Distance']] = scaler.fit_transform(df[['Age', 'Flight Distance']])

# Sélection des features et de la cible
X = df[['Age', 'Class_Business', 'Class_Eco Plus', 'Class_Eco', 'Type of Travel_Business travel', 'Customer Type_Loyal Customer',
     'Flight Distance', 'Online boarding', 'Seat comfort', 'Inflight entertainment', 'On-board service', 'Leg room service',
     'Cleanliness']]

y = df["satisfaction_satisfied"]

# Séparation train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=6, stratify=y)

# Entraînement et évaluation du modèle KNN

# Best k
k_range = range(1, 21)
scores = []
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    scores.append(accuracy_score(y_test, y_pred))
best_k = k_range[scores.index(max(scores))]
print(f"✅ Best k: {best_k} with accuracy: {max(scores):.4f}")

knn = KNeighborsClassifier(n_neighbors=best_k)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
print("KNN evaluation:\n")
print(f"accuracy : {knn.score(X_test, y_test)}")
print(f"confusion matrix : {confusion_matrix(y_test, y_pred)}")
print(f"classification report : {classification_report(y_test, y_pred)}")

# Entraînement et évaluation Logistic Regression
logreg = LogisticRegression()
logreg.fit(X_train, y_train)
y_pred = logreg.predict(X_test)
print("Logistic Regression evaluation:\n")
print(f"accuracy : {logreg.score(X_test, y_test)}")
print(f"confusion matrix : {confusion_matrix(y_test, y_pred)}")
print(f"classification report : {classification_report(y_test, y_pred)}")

"""knn is better"""

# Sauvegarde du modèle KNN
joblib.dump(knn,"satisfaction_knn_model.joblib")
joblib.dump(scaler, "scaler.joblib")

import json
with open("feature_order.json", "w") as f:
    json.dump(list(X.columns), f)