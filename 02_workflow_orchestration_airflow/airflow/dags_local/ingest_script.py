import os
from time import time
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine

def ingest_callable(user, password, host, port, db, table_name, parquet_file, execution_date):
    print(table_name, parquet_file, execution_date)

    # Création de la connexion PostgreSQL
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    print('Connection established successfully, inserting data...')

    t_start = time()

    # Lecture du fichier Parquet en utilisant PyArrow
    parquet_data = pq.ParquetFile(parquet_file)

    # Obtenir les colonnes
    columns = parquet_data.schema.names

    # Lecture et insertion par chunks
    rows_per_chunk = 100000
    batch_index = 0
    for batch in parquet_data.iter_batches(batch_size=rows_per_chunk):
        df = pd.DataFrame(batch.to_pandas())  # Conversion en DataFrame pandas
        
        # Conversion des colonnes de datetime
        if 'tpep_pickup_datetime' in df.columns:
            df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        if 'tpep_dropoff_datetime' in df.columns:
            df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

        # Si premier batch, créer la table
        if batch_index == 0:
            df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')
        
        # Insérer le batch courant
        df.to_sql(name=table_name, con=engine, if_exists='append')

        t_end = time()
        print(f'Inserted batch {batch_index}, took %.3f seconds' % (t_end - t_start))
        batch_index += 1

    print("Data ingestion completed.")
