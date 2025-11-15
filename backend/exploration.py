# Importation des bibliothèques nécessaires
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Chargement des données
df = pd.read_csv("C:/Users/MALAK/OneDrive/Bureau/satisfaction-app/backend/data/train.csv")
print(df.head())
print(df.isna().sum())
print(f"Duplicated rows: {df.duplicated().sum()}")

# Suppression des lignes avec valeurs manquantes faibles
threshold = len(df)*0.05
cols_to_drop = df.columns[df.isna().sum()<=threshold]
df.dropna(subset=cols_to_drop, inplace=True)
df.isna().sum()

# Conversion de types
df["Arrival Delay in Minutes"] = df["Arrival Delay in Minutes"].astype(int)
df.info()
       
# Visualisation des variables qualitatives liées au vol
cols= ['Inflight wifi service','Departure/Arrival time convenient', 'Ease of Online booking','Gate location', 'Food and drink', 
       'Online boarding', 'Seat comfort', 'Inflight entertainment', 'On-board service', 'Leg room service','Baggage handling', 
       'Checkin service', 'Inflight service','Cleanliness']

fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(18, 14))
axes = axes.flatten()

for i, col in enumerate(cols):
    sns.countplot(x=col, data=df, ax=axes[i])
    axes[i].set_title(col)
    axes[i].tick_params(axis='x', rotation=90)

for j in range(len(cols), len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()

# Aperçu statistique
print(df[['Departure Delay in Minutes', 'Arrival Delay in Minutes', 'Flight Distance', 'Age']].describe())

# Taux de satisfaction global
print(df["satisfaction"].value_counts(normalize=True))

#Quels sont les facteurs qui influencent le plus la satisfaction ?

# Analyse satisfaction par type client
df['Customer Type'].value_counts()
sns.countplot(x="Customer Type", data=df)
plt.title("Satisfaction des passagers par type de client")
plt.show()
satisfaction_by_Customer_Type = df.groupby('Customer Type')['satisfaction'].value_counts(normalize=True)
satisfaction_by_Customer_Type.plot(kind="bar")
plt.show()
"""loyal cust>>>disloyal customer and and 0.75% of disloyal customer are not satisfied"""

# Analyse satisfaction par tranche d'âge
df['Tranche_age'] = pd.cut(df['Age'], bins=[0, 25, 40, 60, 100], 
                           labels=['Jeunes', 'Adultes', 'Matures', 'Seniors'])
sns.countplot(x="satisfaction", data=df, hue="Tranche_age")
plt.title("Satisfaction des passagers par tranche d'âge")
plt.show()
satisfaction_by_tranche_age = df.groupby('Tranche_age')['satisfaction'].value_counts(normalize=True)
satisfaction_by_tranche_age.plot(kind="bar")
plt.show()
"""mature people are satisfied and jeunes and seniors are not"""

# Analyse satisfaction par genre
df['Gender'].value_counts(normalize=True) * 100  # en %
sns.countplot(x='Gender', data=df)
plt.title("Répartition des passagers selon le genre")
plt.show()
satisfaction_by_gender = df.groupby('Gender')['satisfaction'].value_counts(normalize=True)
satisfaction_by_gender.plot(kind="bar")
plt.show()
"""equally balance => does not interfere"""

# Analyse satisfaction par classe
df['Class'].value_counts(normalize=True) * 100
sns.countplot(x='Class', data=df)
plt.title("Répartition selon la classe de voyage")
plt.show()
satisfaction_by_class = df.groupby('Class')['satisfaction'].value_counts(normalize=True)
satisfaction_by_class.plot(kind="bar")
plt.show()
"""buisness class are satisfied but others are not"""

# Analyse satisfaction par type de voyage
df['Type of Travel'].value_counts(normalize=True) * 100
sns.countplot(x='Type of Travel', data=df)
plt.title("Type de voyage (affaires / personnel)")
plt.show()
satisfaction_by_type = df.groupby('Type of Travel')['satisfaction'].value_counts(normalize=True)
satisfaction_by_type.plot(kind="bar")
plt.show()
"""nuisness travel are bigger number and are satisfied while personol not satisfied"""

#Y a-t-il des profils types de passagers insatisfaits ?
# Profils types insatisfaits : seniors, jeunes, voyages personnels, pas business class

# Visualisation des retards et distances
for col in ["Departure Delay in Minutes",  "Arrival Delay in Minutes",  "Flight Distance"]:
    sns.boxplot(data=df, x=col)
    plt.show()
    
# Encodage des variables catégorielles importantes
dummies = pd.get_dummies(df[["satisfaction","Customer Type",'Type of Travel','Class']]).astype(int)
df = pd.concat([df,dummies],axis=1)

# Suppression des colonnes inutiles ou redondantes
df = df.drop(['Unnamed: 0', 'id', "Gender", "Customer Type", 'Type of Travel', 'Class',"satisfaction","Class_Eco Plus","Type of Travel_Personal Travel","Customer Type_disloyal Customer","satisfaction_neutral or dissatisfied"],axis=1)

# Heatmap de corrélation
plt.figure(figsize=(14,10))
corr_matrix = df.corr(numeric_only=True)
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm')
plt.title("Corrélation entre les variables")
plt.show()
"""cols<-0.3 et >0.3"""

# Standardisation des variables numériques continues
cols_to_scale = ['Age', 'Flight Distance', 'Departure Delay in Minutes', 'Arrival Delay in Minutes']
scaler = StandardScaler()
df[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])

# Sélection des features et de la cible (selon corrélation + métier)
X = df[['Age', 'Class_Business', 'Class_Eco', 'Type of Travel_Business travel', 'Customer Type_Loyal Customer',
     'Flight Distance', 'Online boarding', 'Seat comfort', 'Inflight entertainment', 'On-board service', 'Leg room service',
     'Cleanliness']]

y = df["satisfaction_satisfied"]

# Séparation des données pour l’entraînement
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=6, stratify=y)

# Entraînement et évaluation du modèle KNN
k_range = range(1, 21)
scores = []

for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    scores.append(accuracy_score(y_test, y_pred))

# Plot
plt.figure(figsize=(10,6))
plt.plot(k_range, scores, marker='o')
plt.title("Accuracy vs. Number of Neighbors (k)")
plt.xlabel("k")
plt.ylabel("Accuracy")
plt.xticks(k_range)
plt.grid()
plt.show(block=False)



