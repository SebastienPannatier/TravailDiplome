# Comment utiliser des graphes de connaissance pour améliorer l'interaction utilisateur-chatbot

## Description

Ce projet est le travail de diplôme de Sébastien Pannatier, étudiant à l'École Supérieure d'Informatique de Gestion (ESIG). Il s'agit d'un projet de recherche qui explore l'utilité des graphes de connaissance dans le cadre de l'amélioration des interactions entre utilisateurs et chatbots.

L'objectif principal de ce travail est d'examiner comment l'intégration de graphes de connaissance peut enrichir les capacités d'un chatbot en lui permettant de fournir des réponses plus pertinentes et contextualisées. Le projet inclut la création d'un chatbot en utilisant Rasa, ainsi qu'un graphe de connaissances implémenté avec TypeDB, et explore la manière dont ces deux composants peuvent être liés pour offrir une expérience utilisateur améliorée.

## Objectifs

- Évaluer l'utilité des graphes de connaissance dans le cadre de l'amélioration de l'interaction utilisateur-chatbot.
- Créer un chatbot capable de répondre à des requêtes complexes en s'appuyant sur un graphe de connaissances.
- Permettre la recherche d'informations sur des restaurants et des hôtels, ainsi que la fourniture de détails pertinents concernant ces établissements.

## Fonctionnalités principales

- Recherche de restaurants et d'hôtels.
- Consultation des détails concernant les restaurants et les hôtels.
- Intégration d'un graphe de connaissances avec TypeDB pour enrichir les réponses du chatbot.

## Technologies utilisées

- **Langages et frameworks** : Python, HTML, CSS, JavaScript
- **Outils et bibliothèques** : Rasa, SpaCy, TypeDB, GitHub
- **Serveurs** : Serveur HTTP (géré avec xpm), Serveur Rasa, Serveur d'action Rasa, Serveur TypeDB

## Architecture du projet

Le projet est organisé en trois répertoires principaux :

- **/Bot** : Contient le code du chatbot Rasa.
- **/Sources** : Contient les fichiers sources pour le graphe de connaissances.
- **/Web** : Contient les fichiers front-end pour l'interface utilisateur.

## Instructions d'installation

1. Clonez le dépôt GitHub :
   ```bash
   git clone https://github.com/SebastienPannatier/TravailDiplome
   ```
2. Installez les dépendances en utilisant le fichier requirements.txt :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

1. Lancez votre serveur TypeDB
   ```bash
   typedb server
   ```
2. Rendez-vous dans le dossier /Sources
   ```bash
   cd Sources
   ```
3. Ajoutez à votre base TypeDB le **schema-agence-voyage.tql**
   ```bash
   typedb console
   ```
   ```bash
   transaction nom_de_votre_base schema write
   ```
   ```bash
   source schema-agence-voyage.tql
   ```
   ```bash
   commit
   ```
4. Executez le script python d'insertion de données
   ```bash
   py migrate.py
   ```
5. Rendez-vous dans le dossier /Bot
   ```bash
   cd Bot
   ```
6. Démarrez le serveur d'actions
   ```bash
   rasa run actions
   ```
7. Démarrez le serveur Rasa
   ```bash
   rasa run --debug --enable-api --cors "*"
   ```
8. Rendez-vous dans le dossier /Web :
   ```bash
   cd Web
   ```
9. Lancez le serveur HTTP avec nxp :
   ```bash
   nxp http-server
   ```
   Une fois tous les serveurs lancés, vous pouvez interagir avec le chatbot via l’interface web. Le chatbot est capable de répondre à des requêtes concernant les restaurants et les hôtels, en fournissant des informations détaillées issues du graphe de connaissances.

## Contributions

Ce projet est privé et n’accepte pas de contributions externes pour le moment.

## Auteurs et crédits

- **Auteur** : Sébastien Pannatier, étudiant à l’ESIG

## Licence

Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus de détails.
