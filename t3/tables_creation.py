import os
import psycopg2
from config import load_config
import json
from datetime import datetime

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

# Função para criar tabela no PostgreSQL
def create_table(conn, table_name):
    cur = conn.cursor()
    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id BIGSERIAL PRIMARY KEY,
        ordem VARCHAR(13),
        latitude DECIMAL(12, 6),
        longitude DECIMAL(12, 6),
        datahora BIGINT,
        velocidade INTEGER,
        linha VARCHAR(10),
        datahoraenvio BIGINT,
        datahoraservidor BIGINT
    );
    '''
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    print(f"Tabela {table_name} criada com sucesso!")

def insert_data(conn, table_name, data):
    cur = conn.cursor()
    insert_query = f'''
    INSERT INTO {table_name} (
        ordem, latitude, longitude, datahora, velocidade, linha, datahoraenvio, datahoraservidor
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    for entry in data:
        ordem = entry['ordem']
        latitude = float(entry['latitude'].replace(',', '.'))
        longitude = float(entry['longitude'].replace(',', '.'))
        datahora = int(entry['datahora'])
        velocidade = int(entry['velocidade'])
        linha = entry['linha']
        datahoraenvio = int(entry['datahoraenvio'])
        datahoraservidor = int(entry['datahoraservidor'])
        cur.execute(insert_query, (
            ordem, latitude, longitude, datahora, velocidade, linha, datahoraenvio, datahoraservidor
        ))
    conn.commit()
    cur.close()
    print(f"Dados inseridos na tabela {table_name} com sucesso!")

# Caminho da pasta principal contendo as subpastas
password = input("Digite a senha do usuário: ")
main_folder_path = '//home/savio/Downloads/T3'
conn = psycopg2.connect(
    dbname="t3",
    user="savio",
    password=password,
    host="localhost",
)

# Navegar pelas subpastas e criar tabelas
for subfolder in os.listdir(main_folder_path):
    subfolder_path = os.path.join(main_folder_path, subfolder)
    if os.path.isdir(subfolder_path):
        day = subfolder[8:10]
        month = subfolder[5:7]
        table_name = f'dia_{day}{month}'
        # Verificar se o nome da tabela é válido no PostgreSQL
        if table_name.isidentifier():
            create_table(conn, table_name)
        else:
            print(f"Nome de subpasta inválido para nome de tabela: {table_name}")
    for arquivo in os.listdir(subfolder_path):
        with open(arquivo, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        
    
    

# Fechar a conexão
conn.close()