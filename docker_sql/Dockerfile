# Utilise une image de base officielle Python version 3.9.1
FROM python:3.9.1

# Installe la bibliothèque pandas avec pip
RUN pip install pandas argparse sqlalchemy pyarrow

# Définit le répertoire de travail à /app dans le conteneur
WORKDIR /app

# Copie le fichier pipeline.py depuis le système hôte vers le conteneur
COPY ingest_data.py ingest_data.py

# Définit le point d'entrée pour exécuter pipeline.py avec Python
ENTRYPOINT [ "python", "ingest_data.py" ]