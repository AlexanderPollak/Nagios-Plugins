# Check APC UPS
Nagios script to check Uninterrupted Power Supply from APC.: tested with Smart-UPS 500

# Requirements:
```
Uses 'snmpget' to aquire data via SNMP v1.:
# installs SNMP package:
sudo apt-get install snmp
# downloads common SNMP MIBs:
sudo apt-get install snmp-mibs-downloader

Note that "PowerNet-MIB.mib" needs to be copied into "/usr/share/snmp/mibs/"
Note that /etc/snmp/snmp.conf needs to be modified:

nano /etc/snmp/snmp.conf 
change in the fourth line "#mibs" to "mibs ALL"
```
# Usage:
```
./check_apc_ups -h [hostname] -c [community] -s [check] -u [units]
```

# Options:
```
    -h  [snmp hostname]   Hostname
    -c  [community name]  community name (ex: public)
    -p  [snmp port]       port for snmp request (default: 161)
    -t  [timeout]	      duration before doing an timeout in seconds - default 10s

    -s  [check]           Check to be executed
        info              System infos
	    status            Check UPS status: [Status]
	    battery           Check the Battery: [Status, Charge, Voltage]
        temperature       Check UPS temperature [Temperature]
	    input             Check input: [Voltage, Current]
	    output            Check output: [Voltage, Current]
	    load              Check UPS load: [Phase Load in %, Total Power]

    -A  [Bat. warning]    Threshold for Battery Charge Warning [Default: 70%]
    -B  [Bat. critical]   Threshold for Battery Charge Critical [Default: 40% ]
    -C  [T. warning]      Threshold for Temperature Warning [Default: 50C]
    -D  [T. critical]     Threshold for Temperature Critical [Default: 60C]
    -E  [Load warning]    Threshold for UPS High Load Warning [Default: 75%]
    -F  [Load critical]   Threshold for UPS High Load Critical [Default: 85%]
    -G  [V. low warn]     Threshold for low input/output Voltage Warning [Default: 110V]
    -H  [V. low crit]     Threshold for low input/output Voltage Critical [Default: 105V]
    -I  [V. high warn]    Threshold for high input/output Voltage Warning [Default: 125V]
    -J  [V. high crit]    Threshold for high input/output Voltage Critical [Default: 130V]
```

# Examples:
```
  ./check_apc_ups -h 1.2.3.4 -c public -s info
  ./check_apc_ups -h 1.2.3.4 -p 4321 -c public -s status -t 30 
  ./check_apc_ups -h 1.2.3.4 -c public -s load 
```

# Example Returns:
```
./check_apc_ups -h 1.2.3.4 -c public -s status 
"OK - UPS Status: Normal"

./check_apc_ups -h 1.2.3.4 -c public -s load 
"OK - UPS load is 9%"
```