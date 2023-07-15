# Check Synology NAS
Nagios script to check Synology NAS.: tested with RS2418RP+

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
# Usage:
```
./check_synology [OPTIONS] -U [user] -P [pass] -h [hostname] -s [check]
```

# Options:
```
-U [snmp username]     Username for SNMPv3
-P [snmp password]     Password for SNMPv3

-2 [community name]    Use SNMPv2 (no need user/password) & define community name (ex: public)

-h [hostname or IP]    Hostname or IP. You can also define a different port
-p [snmp port]         Port for snmp request (default: 161)

-s  [check]           Check to be executed
        info          Show System Infos
        dev_status    Check Device Status
        dev_temp      Check Device Temperature
        disk_status   Check Status for All Disks" 
        disk_temp     Check Temperature for All Disks"       
        raid          Check RAID
        usage         Check Storage Usage
        update        Check for DSM updates
        ups           Show informations about the connected UPS (only information, not tested)

-W [warning degC]      Warning temperature (for disks & synology) [Default: 50degC]
-C [critical degC]     Critical temperature (for disks & synology) [Default: 60degC]

-w [warning %]         Warning storage usage percentage [Default: 80%]
-c [critical %]        Critical storage usage percentage [Default: 95%]


	
```

# Examples:
```
./check_synology -u admin -p 1234 -h 10.1.10.70 -s info	
./check_synology -u admin -p 1234 -h nas.org -s raid 
./check_synology -2 public -h 10.1.10.70 -p 5300 -s disk_status
```
# Example Returns:
```
./check_synology -2 public -h 1.2.3.4 -s dev_status
"System Satus: OK"
```