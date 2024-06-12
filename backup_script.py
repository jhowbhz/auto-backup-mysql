import pymysql
import subprocess
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

import platform  # Módulo para verificar a plataforma do sistema operacional

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Parâmetros do MySQL
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# Parâmetros do FTP
FTP_HOST = os.getenv('FTP_HOST')
FTP_USERNAME = os.getenv('FTP_USERNAME')
FTP_PASSWORD = os.getenv('FTP_PASSWORD')
UPLOAD_DIRECTORY = 'BACKUP'  # Nome da pasta de destino no servidor FTP do BunnyCDN

# Parâmetros do arquivo
FILE_PATH = '/opt'
FILENAME_EXTENSION = 'backup.sql.gz'

# URL da API para enviar dados de progresso
PROGRESS_API_URL = 'http://localhost:5000/progress'

SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

BK_SAVE_PATH = os.path.join(SCRIPT_DIRECTORY, 'Backup')

# Verificar se o diretório de backup existe e criar se não existir
if not os.path.exists(BK_SAVE_PATH):
    os.makedirs(BK_SAVE_PATH, mode=0o777, exist_ok=True)

# Função para enviar progresso para a API
def send_progress(status, progress):
    data = {
        'status': status,
        'progress': progress
    }
    try:
        requests.post(PROGRESS_API_URL, json=data)
    except Exception as e:
        print(f"Erro ao enviar progresso: {e}")

# Função para fazer backup de uma tabela específica
def backup_table(table_name, file_path):
    # Construir o caminho completo para o arquivo de backup
    backup_file = os.path.join(BK_SAVE_PATH, f"{table_name}_{datetime.now().strftime('%Y-%m-%d')}.sql.gz")

    # Verificar a plataforma do sistema operacional
    if platform.system() == 'Windows':
        mysqldump_path = os.path.join(SCRIPT_DIRECTORY, 'Lib', 'mysqldump.exe')
        dump_command = f"{mysqldump_path} -u {MYSQL_USER} --password='{MYSQL_PASSWORD}' -h {MYSQL_HOST} -P {MYSQL_PORT} --single-transaction --quick --lock-tables=true --max-allowed-packet=1G {MYSQL_DATABASE} {table_name} > {backup_file}"
    else:
        dump_command = f"mysqldump -u {MYSQL_USER} --password='{MYSQL_PASSWORD}' -h {MYSQL_HOST} -P {MYSQL_PORT} --single-transaction --quick --lock-tables=true --max-allowed-packet=1G {MYSQL_DATABASE} {table_name} | gzip -9 -f > {backup_file}"

    try:
        subprocess.run(dump_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando de backup para a tabela {table_name}: {e}")

# Função para obter a lista de tabelas do banco de dados
def get_table_list():
    connection = pymysql.connect(
        host=MYSQL_HOST,
        port=int(MYSQL_PORT),
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    table_list = [table[0] for table in tables]
    cursor.close()
    connection.close()
    return table_list

# Criar o nome da pasta com o formato "YYYY-MM-DD"
current_date = datetime.now().strftime('%Y-%m-%d')
folder_name = os.path.join(UPLOAD_DIRECTORY, current_date)

# Definir o caminho completo do arquivo de backup
file_full_path = os.path.join(FILE_PATH, FILENAME_EXTENSION)

# Obter a lista de tabelas do banco de dados
table_list = get_table_list()
total_tables = len(table_list)
tables_backuped = 0

# Enviar progresso inicial
send_progress('Iniciando backup', 0)

# Realizar o backup de cada tabela
for table_name in table_list:
    send_progress(f'Fazendo backup da tabela {table_name}', (tables_backuped / total_tables) * 100)
    backup_table(table_name, file_full_path)
    tables_backuped += 1

# Enviar progresso final
send_progress('Backup concluído', 100)

print('Backup concluído.')
