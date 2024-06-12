# Auto Mysql Bunny
Simple script in python using mysqldump tools, define cron backup your database mysql save in CDN bunny

### Download scripts
```sh
git clone https://github.com/jhowbhz/auto-mysql-bunny.git scripts
```

### Install dependencies
```sh
apt install python3 -y && apt install python3-pip -y
``` 
### Install project
```sh
cd /opt/scripts/ && pip3 install -r requeriments.txt
```

### Credentials
Especifique as suas credenciais do MYSQL e do FTP do Bunny

```sh
cp .env-example .env
```

```sh
nano .env
```

```
MYSQL_HOST=seu_host
MYSQL_PORT=sua_porta
MYSQL_USER=seu_usuario
MYSQL_PASSWORD=sua_senha
MYSQL_DATABASE=seu_banco_de_dados
FTP_HOST=seu_host_ftp
FTP_USERNAME=seu_usuario_ftp
FTP_PASSWORD=sua_senha_ftp
```

### Crontab
Vamos acessar a cron 
```sh
crontab -e
```

### Cron def 03:00 AM
```sh
0 3 * * * python3 /opt/scripts/bk.py
```

### Run
```sh
python /opt/scripts/bk.py
```

### Configure Bunny CDN receive Backup FILES
Get your FTP information

https://bunny.net
