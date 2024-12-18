# Check Thermal Server Shutdown
This program monitors the temperature of the Signal Processing Room at the Hat Creek Radio Observatory and shuts down servers in case of a cooling failure.


# Supported Devices
```
RoomAlert Devices:
        1. 32S
```

# Communication
```
RoomAlert Devices:
	The RoomAlert 32S environment monitor is connected via ethernet. It uses the SNMPv1 protocol
	to read out the relevant register. This program supports the readout of individual regsiters
	representing digital and analog inputs.
```


# CLASS Implementation


## avtech_com: RA32S
```
This module contains classes and functions to establish the communication with the Avtech RoomAlert 32S unit via SNMPv1.

The class in this module ("RA32S") allows the user to communicate with the unit and extract the following registers:

List of extracted values:
    1. Temperature in deg Celcius for any connected sensor. 


List of functions:
	open()
	close()
	is_connected()
	read_analog()
    read_di_temp_c()

```

## mysql_write: MySQL_com
```
This module contains classes and functions to write water level and pump status data into a mysql database.

The class in this module ("mysql_com") allows the user to communicate with the mysql database. Each device then
has its own function which allows to populate the device specific table.

List of functions:
	open()
	close()
	is_connected()
	write_data()
```

# MySQL Database Tables
```
This section describes the implemented tables in the MySQL database.

Pump Data Table:

        DROP TABLE IF EXISTS `pump_data`;
        CREATE TABLE `pump_data` (
            `ts` datetime NOT NULL,
            `water_level` float DEFAULT (NULL),
            `temperature` float DEFAULT (NULL),
            `pump1_status` varchar(16) DEFAULT (NULL),
            `pump2_status` varchar(16) DEFAULT (NULL),
            `pump3_status` varchar(16) DEFAULT (NULL),
            `system_status` varchar(16) DEFAULT (NULL),
            PRIMARY KEY (`ts`),
            KEY `idx` (`ts`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```
# Requirements:
```
Uses 'snmpget' to aquire data via SNMP v1 and v3.:
# installs SNMP package:
sudo apt-get install snmp
# downloads common SNMP MIBs:
sudo apt-get install snmp-mibs-downloader

Note that "Synology_MIB_File.zip" needs to be unpacked and copied into "/usr/share/snmp/mibs/"
Note that /etc/snmp/snmp.conf needs to be modified:

nano /etc/snmp/snmp.conf 
change in the fourth line "#mibs" to "mibs ALL"
```


# Software Installation
```
It is recommended to install the software in the following location: "/usr/local/pump-monitor/"

git clone git@github.com:AlexanderPollak/Pump-Monitor.git /usr/local/pump-monitor/


The configuration file for the control program is located at: "/usr/local/pump-monitor/etc/pm.cfg"
This file contains all settings that are required to adjust the program to the individual configuration.
The main sections are:
	1. COMMUNICATION SETTINGS
	2. GENERAL MONITOR SETTINGS
	5. MySQL SPECIFIC SETTINGS


The required python3 modules are listed in a pip requirement file located at: "/usr/local/pump-monitor/etc/pm-pip-req.txt" 

pip install -r /usr/local/pump-monitor/etc/pm-pip-req.txt



To install the SNMP codefollow these steps:

Uses 'snmpget' to aquire data via SNMP v1 and v3.:
# installs SNMP package:
sudo apt-get install snmp
# downloads common SNMP MIBs:
sudo apt-get install snmp-mibs-downloader

Copy "Pump-Monitor/etc/moxa-e1242-v1.2.mib" into "/usr/share/snmp/mibs/"
Note that /etc/snmp/snmp.conf needs to be modified:

nano /etc/snmp/snmp.conf 
change in the fourth line "#mibs" to "mibs ALL"



To install the MySQL database follow these steps:


Step 1 — Installing MySQL

apt update
apt install mysql-server
systemctl enable mysql.service
systemctl start mysql.service
systemctl status mysql.service


Step 2 — Configuring MySQL

mysql
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
mysql> exit
mysql_secure_installation

mysql -u root -p
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH auth_socket;


Step 3 — Creating a Dedicated MySQL User and Granting Privileges

mysql
mysql> CREATE USER 'grafana'@'localhost' IDENTIFIED WITH authentication_plugin BY 'password';


Step 4 - Create new database called: pmdata

mysql
mysql> CREATE DATABASE pumpdata;


Step 5 - Create a New User and Grant Permissions in MySQL

mysql
mysql> CREATE USER 'grafanauser'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
mysql> GRANT ALL on pumpdata.* TO 'grafanauser'@'localhost';
mysql> FLUSH PRIVILEGES;


Step 6 - Create a tables in database pumpdata

mysql pumpdata < /usr/local/pump-monitor/etc/pm-data.sql





To install the Grafana data visualization follow these steps:


Step 1 — Install Grafana

wget -q -O - https://packages.grafana.com/gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/grafana.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/grafana.gpg] https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
apt update
apt install grafana
systemctl start grafana-server
systemctl enable grafana-server
systemctl status grafana-server


Step 2 — Install Solar Control Dashboard


Click Dashboards in the left-side menu.
Click New and select Import in the dropdown menu.
Upload dashboard JSON file from: "/usr/local/solar-control-program/etc/scp-dashboard.json"


```


# Usage:
```
Run the executable shell script in a screen session.

screen -R scp
/usr/local/pump-monitor/Pump-Monitor-Program.sh
Crtl-A D

To reconnect to the screen session execute:

screen -r scp
```

