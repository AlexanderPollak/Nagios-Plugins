# Check Mitsubishi UPS
Nagios script to check Liebert HVAC.: tested with DS070ASAOEI

# Requirements:
```
Uses 'snmpget' to aquire data via SNMP v1.:
# installs SNMP package:
sudo apt-get install snmp
# downloads common SNMP MIBs:
sudo apt-get install snmp-mibs-downloader

Note that "LIEBERT_GP_REG.mib", "LIEBERT_GP_ENV.mib", "LIEBERT_GP_AGENT.mib", and "LIEBERT_GP_COND.mib"
needs to be copied into "/usr/share/snmp/mibs/"
Note that /etc/snmp/snmp.conf needs to be modified:

nano /etc/snmp/snmp.conf 
change in the fourth line "#mibs" to "mibs ALL"
```
# Usage:
```
./check_Liebert_hvac -h [hostname] -c [community] -s [check]
```

# Options:
```
-h  [snmp hostname]       hostname
-c  [community name]      community name (ex: public)
-p  [snmp port]           port for snmp request (default: 161)
-t  [timeout]	          duration before doing an timeout in seconds - default 10s

-s  [check]               Check to be executed
    info                  System infos
    runtime               Show Runtime: [Comp1, Comp2, Heater, Humidify, Dehumidify]
    hvac_status           Check HVAC Status: [System, Cooling, Heating, Fan, Humidify, Dehumidify]
    hvac_alarm            Check HVAC Alarm: [Alarm]
    hvac_capacity         Check Current Capacity: [Cooling, Heating]
    hvac_temp_return      Check Current Return Temp: [Measured Temp, Setpoint Temp]
    hvac_temp_control     Check Current Control Temp: [Measured Temp, Setpoint Temp]
    hvac_humidity_return  Check Current Return Humidity: [Measured Humidity, Setpoint Humidity]
    hvac_humidity_control Check Current Control Humidity: [Measured Humidity, Setpoint Humidity]
    comp_temp             Check Compressor Temparature: [Comp1, Comp2]

-C  [Comp. temp warning]    Threshold for Compressor High Temperature Warning [Default:120degC]
-D  [Comp. temp critical]   Threshold for Compressor High Temperature Critical [Default:130degC]
```

# Examples:
```
./check_liebert_hvac -h 1.2.3.4 -c public -s info
./check_liebert_hvac -h 1.2.3.4 -p 4321 -c public -s runtime
./check_liebert_hvac -h 1.2.3.4 -c public -s comp_temp -C 100 -D 110
```
# Example Returns:
```
./check_liebert_hvac -h 1.2.3.4 -p 4321 -c public -s runtime
"HVAC Runtimes - Comp1.=16776h - Comp2.=16793h - Humidifier=1286h - Dehumidifier=6271h - Heater1=35h - Heater2=37h - Heater3=34h"

./check_mitsubishi_ups -h 1.2.3.4 -c public -s comp_temp
"OK - Comp.1=64degC - Comp.2=29degC"
```