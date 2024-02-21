# Nagios-Plugins
This Repository contains a number of Nagios Plugins tested with Nagios Core 4.4.13

# List of Plugins:
```
- Check APC Power Distribution Units
- Check Liebert HVAC
- Check Mitsubishi UPS
- Check Netgear NAS
- Check Netgear Switch
- Check Avtech RoomAlert 12S
- Check Disk Health: smartctl
- Check Raid Controller: storcli
- Check Supermicro Hardware IPMI
- Check Synology NAS
```

# Configure and Install Nagios 4 with Nginx on Ubuntu 22.04:
```
#Step 1 — Update System

apt update
apt upgrade -y


#Step 2 — Install Nagios Core

apt install wget unzip curl openssl build-essential libgd-dev libssl-dev php8.1 php8.1-fpm fcgiwrap php8.1-gd -y
cd /tmp/
wget https://assets.nagios.com/downloads/nagioscore/releases/nagios-4.4.13.tar.gz
tar -zxvf nagios-4.4.13.tar.gz
cd nagios-4.4.13/
./configure
make all

make install-groups-users
usermod -a -G nagios www-data

make all
make install
make install-init
make install-commandmode
make install-config

apt install apache2-utils
htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin


#Step 3 - Configure nginx

nano /etc/nginx/sites-available/nagios.conf

"
server {
    server_name     nagios.lm;
    root            /usr/local/nagios/share;

    listen 443 ssl http2 ;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers "HIGH:!aNULL:!MD5 or HIGH:!aNULL:!MD5:!3DES";
    ssl_prefer_server_ciphers on;
    ssl_session_timeout 5m;
    ssl_certificate /etc/nginx/certs/wildcard-lm.crt;
    ssl_certificate_key /etc/nginx/certs/wildcard-lm.key;
    add_header Strict-Transport-Security "max-age=31536000";

    index           index.php index.html index.htm;
    access_log      /var/log/nginx/nagios.access.log;
    error_log       /var/log/nginx/nagios.error.log;

    auth_basic            "Nagios Access";
    auth_basic_user_file  /usr/local/nagios/etc/htpasswd.users;

    # Fixes frames not working
    add_header X-Frame-Options "ALLOW";

    location ~ \.php$ {
        try_files       $uri = 404;
        fastcgi_index   index.php;
        fastcgi_pass    unix:/run/php/php8.1-fpm.sock;
        include         fastcgi.conf;
    }

    location ~ \.cgi$ {
        root            /usr/local/nagios/sbin;
        rewrite         ^/nagios/cgi-bin/(.*)\.cgi /$1.cgi break;
        fastcgi_param   AUTH_USER $remote_user;
        fastcgi_param   REMOTE_USER $remote_user;
        include         fastcgi.conf;
        fastcgi_pass    unix:/run/fcgiwrap.socket;
    }

    # Fixes the fact some links are expected to resolve to /nagios, see here.
    location /nagios {
        alias /usr/local/nagios/share;
    }
}
"


#Step 4 — Install Nagios Plugins

cd /tmp
wget https://nagios-plugins.org/download/nagios-plugins-2.4.4.tar.gz
tar -xvf nagios-plugins-2.4.4.tar.gz 
cd nagios-plugins-2.4.4/
./configure 
make
make install
chown nagios.nagios /usr/local/nagios
chown -R nagios.nagios /usr/local/nagios/libexec/


#Step 5 — Restart Nagios Core

systemctl enable nagios.service
systemctl restart nagios.service
```