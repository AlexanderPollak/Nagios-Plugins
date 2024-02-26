# Check Avtech RoomAlert 32S
Nagios script to check Avtech RoomAlert.: tested with 32S

# Requirements:
```
Uses 'snmpget' to aquire data via SNMP v1.:
# installs SNMP package:
sudo apt-get install snmp
# downloads common SNMP MIBs:
sudo apt-get install snmp-mibs-downloader

Note that "ROOMALERT32S.MIB" needs to be copied into "/usr/share/snmp/mibs/"
Note that /etc/snmp/snmp.conf needs to be modified:

nano /etc/snmp/snmp.conf 
change in the fourth line "#mibs" to "mibs ALL"
```
# Usage:
```
./check_avtech_32S -h [hostname] -c [community] -s [check]
```

# Options:
```
-h  [snmp hostname]   Hostname
-c  [community name]  community name (ex: public)
-p  [snmp port]       port for snmp request (default: 161)
-t  [timeout]	      duration before doing an timeout in seconds - default 10s

-d  [sensor number]   Sensor id number to check [0-8]
                      0 is for the internal sensor
                      
-s  [check]           Check to be executed
    info              System infos
    temp              Check Temperature Sensor
    hum               Check Humidity Sensor

-A  [Temp. High warning]   Threshold for Temperature Sensor High Warning [Default: 25degC]
-B  [Temp. High critical]  Threshold for Temperature Sensor High Critical [Default: 30degC]
-C  [Temp. Low warning]    Threshold for Temperature Sensor Low Warning [Default: 7degC]
-D  [Temp. Low critical]   Threshold for Temperature Sensor Low Critical [Default: 5degC]
-E  [Hum. High warning]    Threshold for Humidity Sensor High Warning [Default: 60%]
-F  [Hum. High critical]   Threshold for Humidity Sensor High Critical [Default: 70%]
-G  [Hum. Low warning]     Threshold for Humidity Sensor Low Warning [Default: 20%]
-H  [Hum. Low critical]    Threshold for Humidity Sensor Low Critical [Default: 10%]
```

# Examples:
```
./check_avtech_32S -h 1.2.3.4 -c public -s info

Temperature value of external sensor 1:
./check_avtech_32S -h 1.2.3.4 -p 4321 -c public -d 1 -s temp

Humidity value of internal sensor:
./check_avtech_32S -h 1.2.3.4 -p 4321 -c public -d 0 -s hum
```
# Example Returns:
```
./check_avtech_32S -h 1.2.3.4 -c public -d 1 -s temp
"OK - Temperature: 18.7degC"

./check_avtech_32S -h 1.2.3.4 -p 4321 -c public -d 0 -s hum
"OK - Humidity: 30.9%"
```
