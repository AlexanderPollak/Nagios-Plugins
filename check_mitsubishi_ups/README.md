# Check Mitsubishi UPS
Nagios script to check Mitsubishi UPS.: tested with UP9933A

# Requirements:
```
Uses 'snmpget' to aquire data via SNMP v1.:
# installs SNMP package:
sudo apt-get install snmp
# downloads common SNMP MIBs:
sudo apt-get install snmp-mibs-downloader

Note that "MITSUBISHI-UPS-MIB.mib" needs to be copied into "/usr/share/snmp/mibs/"
Note that /etc/snmp/snmp.conf needs to be modified:

nano /etc/snmp/snmp.conf 
change in the fourth line "#mibs" to "mibs ALL"
```
# Usage:
```
./check_mitsubishi_ups -h [hostname] -c [community] -s [check]
```

# Options:
```
-h  [snmp hostname]   Hostname
-c  [community name]  community name (ex: public)
-p  [snmp port]       port for snmp request (default: 161)
-t  [timeout]	      duration before doing an timeout in seconds - default 10s

-s  [check]           Check to be executed
	info              System infos
	battery_status    Check the Battery status: [Status]
	battery_charge    Check the Battery status: [Charge, Voltage]
	input_voltage     Check input: [Voltage]
	output_voltage    Check output: [Voltage]
	output_current    Check output: [Current]
	ups_load          Check UPS status: [Phase Load in %, Total Power]
	ups_status        Check UPS status: [Status]

-A  [Bat. warning]    Threshold for Battery Charge Warning [Default: 70%]
-B  [Bat. critical]   Threshold for Battery Charge Critical [Default: 40% ]
-U  [Vol. warning]    Threshold for Input / Output Low Voltage Warning [Default: 473V]
-V  [Vol. critical]   Threshold for Input / Output Low Voltage Critical [Default: 470V]
-C  [Cur. warning]    Threshold for Output High Current Warning [Default: 90A]
-D  [Cur. critical]   Threshold for Output High Current Critical [Default: 102A]
-K  [Load warning]    Threshold for UPS High Load Warning [Default: 75%]
-L  [Load critical]   Threshold for UPS High Load Critical [Default: 85%]
```

# Examples:
```
./check_mitsubishi_ups -h 1.2.3.4 -c public -s info
./check_mitsubishi_ups -h 1.2.3.4 -p 4321 -c public -s battery_status
./check_mitsubishi_ups -h 1.2.3.4 -c public -s ups_status
```
# Example Returns:
```
./check_mitsubishi_ups -h 1.2.3.4 -c public -s battery_status
"OK - Battery Status: Normal"

./check_mitsubishi_ups -h 1.2.3.4 -c public -s ups_load
"OK - Total Load: 40.1kw - UPS Phase Load: L1=41% L2=44% L2=46%"
```