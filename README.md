# SRS_SQL 🚀

## Description 📝
SRS_SQL est une application web permettant d'apprendre et de **retenir efficacement** les commandes SQL grâce à un système de répétition espacée. Le principe est inspiré des cartes Anki 🃏 : plus un exercice est réussi facilement, moins il est reproposé souvent.

## Fonctionnalités 🎯
- **🔐 Authentification** : connexion à l'application.
- **📌 Sélection des exercices** : l'exercice proposé en priorité est le moins récent que l'on a effectué.
- **🧑‍💻 Exercices SQL** :
  - 📂 Tables disponibles fournies.
  - 🎯 Une table cible à obtenir.
  - ✍️ Une requête SQL à écrire from scratch pour obtenir la table cible.
- **⏳ Système de répétition espacée** : gestion intelligente de la récurrence des exercices en fonction des performances.

## Installation ⚙️
### Prérequis 🛠️
- Python 3.8+
- Poetry

### Installation du projet 💻
1. **Cloner le dépôt**
   ```sh
   git clone <URL_DU_REPO>
   cd SRS_SQL
   ```
2. **Installer les dépendances**
   ```sh
   poetry install
   ```
3. **Lancer l'application**
   ```sh
   poetry run streamlit run app.py
   ```

## Utilisation 🎮
1. **🔑 Se connecter à l'application**.
2. **📋 Choisir un exercice** (par défaut, l'exercice le moins récent).
3. **✏️ Réaliser l'exercice** en écrivant une requête SQL correcte.
4. **✅ Valider et voir son score**.
5. **📈 Suivre la progression** avec la répétition espacée.

## Contribuer 🤝
1. **Forker le projet** 🍴
2. **Créer une branche** (`feature/ma_fonctionnalite`)
3. **Commiter les modifications** (`git commit -m "Ajout de X"`)
4. **Pousser la branche** (`git push origin feature/ma_fonctionnalite`)
5. **Créer une Pull Request**

## Licence 📜
Projet sous licence MIT.

---
Tout retour ou contribution est le bienvenu ! 🚀🔥


