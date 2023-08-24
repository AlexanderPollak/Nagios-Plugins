# Check Netgear NAS
Nagios script to check Netgear NAS.: tested with ReadyNAS 6.10.8

# Requirements:
```
Uses 'snmpget' to aquire data via SNMP v1 and v3.:
# installs SNMP package:
sudo apt-get install snmp
# downloads common SNMP MIBs:
sudo apt-get install snmp-mibs-downloader

Note that "netgear.mib" needs to be copied into "/usr/share/snmp/mibs/"
Note that /etc/snmp/snmp.conf needs to be modified:

nano /etc/snmp/snmp.conf 
change in the fourth line "#mibs" to "mibs ALL"
```
# Usage:
```
./check_netgear_nas [OPTIONS] -U [user] -P [pass] -h [hostname] -s [check]
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
        disk_status   Check Status for All Disks
        disk_temp     Check Temperature for All Disks  
        raid          Check RAID
        usage         Check Storage Usage

-W [warning degC]      Warning temperature (for disks & synology) [Default: 50degC]
-C [critical degC]     Critical temperature (for disks & synology) [Default: 60degC]

-w [warning %]         Warning storage free space percentage [Default: 20%]
-c [critical %]        Critical storage free space percentage [Default: 5%]

-r [warning count]     Warning count for Reallocated Sectors [Default: 1]
-l [critical count]    Critical count for Reallocated Sectors [Default: 10]


	
```

# Examples:
```
./check_netgear_nas -u admin -p 1234 -h 10.1.10.70 -s info	
./check_netgear_nas -u admin -p 1234 -h nas.org -s raid 
./check_netgear_nas -2 public -h 10.1.10.70 -p 5300 -s disk_status
```
# Example Returns:
```
./check_netgear_nas -2 public -h 1.2.3.4 -s disk_status
"Number of Disks: 4  -  Status: [OK]"
```