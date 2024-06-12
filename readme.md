## Download scripts
```sh
git clone https://YOUR_KEY_GITHUB@github.com/APIBrasil/apigratis-scripts scripts
```

### Install dependencies
```sh
apt install python3 -y && apt install python3-pip -y
``` 
### Install project
```sh
cd /opt/scripts/backup/ && pip3 install -r requirements.txt
```

### Crontab
Vamos acessar a cron 
```sh
crontab -e
```

### Cron def 03:00 AM
```sh
0 3 * * * python3 /opt/scripts/backup/bk.py
```

### Run
```sh
python /opt/scripts/backup/bk.py
```

### Configure Bunny CDN receive Backup FILES
Get your FTP information

https://bunny.net