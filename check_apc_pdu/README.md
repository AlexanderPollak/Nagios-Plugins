# Check APC PDU
Nagios script to check Power Distribution Module from APC.: tested with AP8941, AP8930, AP7901B

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
./check_apc_pdu -h [hostname] -c [community] -s [check] -u [units]
```

# Options:
```
  -h [snmp hostname]	Hostname
  -c [community name]	community name (ex: public)
  -p [snmp port]	port for snmp request (default: 161)
  -s [check]		Check to be executed
    info		System infos
    psu			Check the status of both Power Supply Units in PDU
    load		Check the load current against the over current thresholds
  -u [units]            Specify number of units that are cascaded [1 or 2]
                        (support for 2 units is implemented)
  -t [timeout]		duration before doing an timeout in seconds - default 10s
```

# Examples:
```
  ./check_apc_pdu -h 1.2.3.4 -c public -s info -u 1
  ./check_apc_pdu -h 1.2.3.4 -p 4321 -c public -s psu -t 30 -u 1
  ./check_apc_pdu -h 1.2.3.4 -c public -s load -u 2
```
# Example Returns:
```
./check_apc_pdu -h 1.2.3.4 -c public -s psu -u 1
"OK - PDU Power Supply Units: 1=OK 2=OK"

./check_apc_pdu -h 1.2.3.4 -c public -s load -u 1
"OK - Load current is lower then threshold: - Load=8.1A  Warning=22A  Critical=24A"
```