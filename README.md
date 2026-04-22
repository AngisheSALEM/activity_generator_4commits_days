# activity_generator_4commits_days


Ce script Python permet d'automatiser la génération de commits sur un dépôt GitHub afin de simuler une activité régulière. Cette version a été configurée pour répondre à des besoins spécifiques de fréquence de commit.

## 🚀 Fonctionnalités
- Génère automatiquement **4 commits par jour** sur l'année écoulée.
- Inclut des exceptions aléatoires : **5 jours à 20 commits** et **2 jours à 13 commits** pour un rendu plus naturel sur le graphe d'activité.
- Permet de définir un dépôt distant pour envoyer l'activité instantanément.

## 📥 Installation

1. **Télécharger le script** :
   Vous devez d'abord récupérer le fichier source. Faites un clic droit sur le lien ci-dessous et choisissez "Enregistrer la cible du lien sous" :
   
   > [📥 Télécharger contribute.py](https://raw.githubusercontent.com/AngisheSALEM/activity_generator_4commits_days/main/contribute.py)  
   *(Note : Assurez-vous de remplacer ce lien par l'URL Raw réelle de votre dépôt)*

2. **Pré-requis** :
   - Python 3 installé.
   - Git configuré avec une clé SSH sur votre machine (ou Codespace).

## 💻 Utilisation

Ouvrez votre terminal et exécutez la commande suivante :

```bash
python3 contribute.py --repository=git@github.com:VOTRE_NOM_UTILISATEUR/VOTRE_REPO.git
