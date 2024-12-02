# 🤖 NeutralAI Bot

NeutralAI Bot est un bot conçu pour classifier les commentaires et générer des réponses spirituelles sur la plateforme Bluesky. Il utilise l'API Mistral pour effectuer des classifications et générer des réponses.

Une version active du bot est disponible sur Bluesky : [neutralai.bsky.social](https://bsky.app/profile/neutralai.bsky.social). Mentionnez simplement le bot sur Bluesky pour le déclencher.

## 🚀 Prérequis

- Docker 🐳
- Docker Compose 🐙
- Python 3.11 🐍

## 🛠️ Installation

1. Clonez ce dépôt :
    ```bash
    git clone https://github.com/votre-utilisateur/neutralaibot.git
    cd neutralaibot
    ```

2. Créez un fichier `.env` à la racine du projet et ajoutez vos identifiants :
    ```env
    ATP_AUTH_HANDLE=votre_handle
    ATP_AUTH_PASSWORD=votre_mot_de_passe
    MISTRAL_API_KEY=votre_cle_api_mistral
    ```

3. Construisez et lancez les services Docker :
    ```bash
    docker-compose up --build
    ```

## 📈 Utilisation

Le bot va automatiquement se connecter à la plateforme Bluesky, récupérer les mentions, classifier les commentaires et répondre aux mentions avec des réponses spirituelles ou des classifications.

### Mode Normal

Le bot analyse les commentaires mentionnés et les classe dans des catégories spécifiques telles que "racist", "sexist", "neutral", etc. en utilisant l'API Mistral. Les résultats de la classification sont ensuite utilisés pour générer des réponses appropriées.

### Mode Witty

En plus de classifier les commentaires, le bot peut également générer des réponses spirituelles et humoristiques. Lorsqu'un commentaire ne nécessite pas de classification, le bot utilise l'API Mistral pour créer une réponse courte et amusante basée sur le texte de la mention.

## 📂 Structure du projet

- `main.py` : Point d'entrée principal du bot.
- `classifier.py` : Contient la classe `CommentClassifier` pour classifier les commentaires et générer des réponses.
- `credentials.py` : Gère le chargement des identifiants et la connexion à la plateforme Bluesky.
- `notifications.py` : Gère la récupération et la mise à jour des notifications.
- `reply.py` : Gère l'envoi des réponses aux mentions.

## 📦 Dépendances

Les dépendances Python sont listées dans le fichier `requirements.txt` :
```txt
requests
python-dotenv
```

## 🤝 Contribution
Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue pour discuter des changements que vous souhaitez apporter.