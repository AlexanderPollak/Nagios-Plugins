# Check RAID Controller
Nagios script to check RAID Controller via storcli /perccli.:

tested with:

007.1804.0000.0000_Unified_StorCLI / Perccli_7.1020.0000_Linux

# Requirements:
```
Uses 'storcli' to aquire data from RAID Controllers.:
# install storcli64 package:

apt install rpm
apt install alien

unzip 007.1804.0000.0000_Unified_StorCLI.zip
cd Unified_storcli_all_os/Linux
rpm --import pubKey.asc
alien -iv storcli-007.1804.0000.0000-1.noarch.rpm

# install perccli64 package:

apt install rpm
apt install alien

tar -xzf Perccli_7.1020.0000_Linux.tar.gz
cd Linux-7.1020
alien -iv perccli-007.1020.0000.0000-1.noarch.rpm

Adjust the path to either storcli64 or perccli64 at the top of the script and for visudo.

# This script needs to run as sudo, to enable Nagios NRPE to
# execute it as sudo without a password add following to "visudo"

visudo
"# Added for Nagios RAID controller checks
nagios ALL=NOPASSWD: /opt/MegaRAID/storcli/storcli64"
```
# Usage:
```
./check_storcli -p /opt/MegaRAID/storcli/storcli64 -s [check]
```

# Options:
```
-p  [path]            Specifies the path to StorCLI, default [/opt/MegaRAID/storcli/storcli64]
-s  [check]           Check to be executed
	  
	  info              Show raid controller infos 
	  battery           Check battery backup unit
	  disk_l            Check disk status, show individual disks
	  disk_s            Check disk status, show summary     
	  raid_l            Check raid status, show individual raids
	  raid_s            Check raid status, show summary
	  ctl               Check raid controller status	
```

# Examples:
```
./check_storcli -s info	
./check_storcli -s raid_s
```
# Example Returns:
```
./check_storcli -s disk_s
"Number of Disks: 124 - Status: [OK]"
```