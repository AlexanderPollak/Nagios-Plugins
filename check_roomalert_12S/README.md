# Check Avtech RoomAlert 12S
Nagios script to check Avtech RoomAlert.: tested with 12S

# Requirements:
```
Uses 'snmpget' to aquire data via SNMP v1.:
# installs SNMP package:
sudo apt-get install snmp
# downloads common SNMP MIBs:
sudo apt-get install snmp-mibs-downloader

Note that "ROOMALERT12S.MIB" needs to be copied into "/usr/share/snmp/mibs/"
Note that /etc/snmp/snmp.conf needs to be modified:

nano /etc/snmp/snmp.conf 
change in the fourth line "#mibs" to "mibs ALL"
```
# Usage:
```
./check_avtech_12S -h [hostname] -c [community] -s [check]
```

# Options:
```
-h  [snmp hostname]   Hostname
-c  [community name]  community name (ex: public)
-p  [snmp port]       port for snmp request (default: 161)
-t  [timeout]	      duration before doing an timeout in seconds - default 10s

-s  [check]           Check to be executed
    info              System infos
    int_temp          Check Device internal Temperature Sensor
    ext_temp          Check External Temperature sensor [Connected to Analog Input 1]

-A  [Temp. High warning]   Threshold for Temperature Sensor High Warning [Default: 23degC]
-B  [Temp. High critical]  Threshold for Temperature Sensor High Warning [Default: 25degC]
-C  [Temp. Low warning]    Threshold for Temperature Sensor Low Warning [Default: 7degC]
-D  [Temp. Low critical]   Threshold for Temperature Sensor Low Warning [Default: 5degC]
```

# Examples:
```
./check_avtech_12S -h 1.2.3.4 -c public -s info
./check_avtech_12S -h 1.2.3.4 -p 4321 -c public -s int_temp
./check_avtech_12S -h 1.2.3.4 -c public -s ext_temp
```
# Example Returns:
```
./check_avtech_12S -h 1.2.3.4 -c public -s int_temp
"OK - Temperature: 18.7degC"
```