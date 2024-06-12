from ftplib import FTP
import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv

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

# Criar o nome da pasta com o formato "YYYY-MM-DD"
current_date = datetime.now().strftime('%Y-%m-%d')
folder_name = os.path.join(UPLOAD_DIRECTORY, current_date)

# Definir o caminho completo do arquivo de backup
file_full_path = os.path.join(FILE_PATH, FILENAME_EXTENSION)

# Comando para fazer o backup do banco de dados usando mysqldump e comprimi-lo com gzip
dump_command = f"mysqldump -u {MYSQL_USER} --password='{MYSQL_PASSWORD}' -h {MYSQL_HOST} -P {MYSQL_PORT} --single-transaction --quick --lock-tables=true --max-allowed-packet=1G {MYSQL_DATABASE} | gzip -9 -f > {file_full_path}"

# Executar o comando
subprocess.run(dump_command, shell=True, check=True)

# Conectar ao servidor FTP do BunnyCDN
ftp = FTP(FTP_HOST)
ftp.login(user=FTP_USERNAME, passwd=FTP_PASSWORD)

# Verificar se a pasta com o nome atual existe, se não, criá-la
if not ftp.nlst(folder_name):
    ftp.mkd(folder_name)

# Mudar para a pasta criada
ftp.cwd(folder_name)

# Abrir o arquivo localmente e fazer upload para o FTP do BunnyCDN
with open(file_full_path, 'rb') as file:
    ftp.storbinary(f'STOR {FILENAME_EXTENSION}', file)

# Fechar a conexão FTP
ftp.quit()

print('Upload do arquivo concluído.')
