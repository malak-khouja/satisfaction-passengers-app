# Analyse de la Satisfaction des Passagers - Projet SkyAir

---

## 🧠 Problématique

La compagnie aérienne **SkyAir** souhaite mettre en place une solution annuelle d'analyse de la satisfaction de ses clients.  
Des enquêtes sont collectées après chaque vol et enregistrées dans un fichier CSV. L'objectif de cette étude est double :

- Fournir un tableau de bord interactif permettant de visualiser les tendances et les points faibles.
- Déployer un modèle de Machine Learning capable de prédire la satisfaction d'un passager à partir de ses caractéristiques.

---

## 🎯 Objectifs de l’analyse

1. Déterminer le **taux de satisfaction global** des passagers.
2. Identifier les **facteurs les plus influents** sur la satisfaction.
3. Déterminer si certaines **catégories de passagers sont plus insatisfaites**.
4. Identifier les **variables explicatives pertinentes** pour l'entraînement du modèle prédictif.

---

## 📌 Données utilisées

- Fichier : `backend/data/train.csv`
- Taille du jeu de données : 103904 lignes (après nettoyage)
- Cibles : `satisfaction` (satisfied vs neutral or dissatisfied)
- Variables explicatives : démographiques, services à bord, retards, fidélité, etc.

---

## 🔍 Nettoyage & Préparation

- Suppression des lignes avec valeurs manquantes inférieures à 5%
- Conversion de la variable `Arrival Delay in Minutes` en entier
- Création d’une variable `Tranche_age` catégorisant l'âge en 4 tranches : Jeunes, Adultes, Matures, Seniors
- Encodage des variables catégorielles (`satisfaction`, `Customer Type`, `Type of Travel`, `Class`) via `pd.get_dummies()`
- Suppression des colonnes inutiles ou redondantes
- Standardisation des variables numériques continues (`Age`, `Flight Distance`, `Departure Delay in Minutes`, `Arrival Delay in Minutes`)

---

## 📊 Analyse exploratoire des données

### 1. Taux de satisfaction global

- 56% des passagers sont satisfaits
- 44% sont neutres ou insatisfaits

Le taux montre une marge d’amélioration significative.

### 2. Impact du type de client

- Les clients **fidèles** ont un taux de satisfaction bien plus élevé.
- Les clients **non fidèles** sont majoritairement insatisfaits.

### 3. Impact de l’âge

- Les **matures (40–60 ans)** sont les plus satisfaits.
- Les **jeunes (<25 ans)** et les **seniors (>60 ans)** sont plus insatisfaits.

### 4. Impact du genre

- Aucune différence significative entre hommes et femmes.

### 5. Classe de voyage

- Les passagers en **classe Business** sont largement plus satisfaits.
- Les passagers en **classe Économique** sont majoritairement insatisfaits.

### 6. Type de voyage

- Les voyages d’affaires sont associés à une satisfaction plus élevée.
- Les voyages personnels génèrent plus d’insatisfaction.

### 7. Services à bord influents

Les variables les plus corrélées avec la satisfaction (corrélation > 0.3) sont :

- `Online boarding`
- `Seat comfort`
- `Inflight entertainment`
- `On-board service`
- `Leg room service`
- `Cleanliness`

---

## 🤖 Modélisation et évaluation

### Préparation des données

- Sélection des variables explicatives pertinentes
- Standardisation des variables numériques
- Séparation des données en jeu d’entraînement et de test (70/30)

### Modèles testés

1. **K-Nearest Neighbors (KNN)**  
   - Recherche du meilleur nombre de voisins (k de 1 à 20)
   - Meilleur k = 15 avec précision d'environ 80%
   - Évaluation avec matrice de confusion et rapport de classification

2. **Régression logistique**  
   - Précision légèrement inférieure (~75%)
   - Évaluation complète similaire

### Résultats

| Modèle               | Accuracy (%) | Commentaire                         |
|----------------------|--------------|-----------------------------------|
| KNN (k=15)           | ~80          | Meilleure performance globale     |
| Régression logistique | ~75          | Modèle simple mais moins performant|

### Conclusion modèle

KNN est retenu pour son meilleur équilibre entre rappel et précision sur ce dataset.

---

## 🧮 Concepts mathématiques appliqués

- Statistiques descriptives (moyennes, distributions, boxplots)
- Analyse de corrélation (coefficients de Pearson)
- Encodage et standardisation des variables pour modélisation
- Algorithme KNN : classification supervisée basée sur la distance
- Régression logistique : modèle probabiliste de classification binaire
- Validation par séparation train/test pour éviter l’overfitting

---

## 🔎 Profils types d’insatisfaits

- Passagers jeunes (<25 ans) ou seniors (>60 ans)
- Voyageurs personnels
- Clients non fidèles
- Passagers en classe économique
- Mauvaises notes sur le confort et les services à bord

---

## 🧾 Conclusion générale

L’analyse permet de cibler précisément les points d’amélioration des services SkyAir.  
Les profils insatisfaits identifiés peuvent faire l’objet d’actions ciblées pour améliorer leur expérience.  

Le modèle KNN prédit avec une bonne précision la satisfaction des passagers, ouvrant la voie à un outil décisionnel pour la compagnie.  

Ce projet illustre l’importance de la combinaison d’analyses statistiques et de modélisation prédictive dans un contexte métier réel.

---

> Projet réalisé par **Malak Khouja** – Août 2025  
> Contact : malak.khouja@example.com  
>  
> *Données : SkyAir - Dataset passagers*  
> *Technologies : Python, Pandas, Seaborn, Scikit-learn*

---

# Annexes

## Visualisations clés

- Graphiques des taux de satisfaction par catégorie
- Heatmap des corrélations
- Courbe de précision en fonction de k (KNN)

---

## Code source

Le code complet est disponible dans le dossier `backend/notebooks/exploration.ipynb`  
Le modèle sauvegardé est dans `backend/models/knn_model.joblib`  

---