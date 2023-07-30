# Check SMART Disk Health
Nagios script to check Disk Health via smartctl.:

tested with: smartctl 7.1 2019-12-30



# Requirements:
```
Uses 'smartctl' to aquire SMART information from Disk.:
# install smartctl package:

apt install smartmontools


# This script needs to run as sudo, to enable Nagios NRPE to
# execute it as sudo without a password add following to "visudo"

visudo
"# Added for Nagios SMART disk checks
nagios ALL=NOPASSWD: /usr/sbin/smartctl"
```
# Usage:
```
./check_smartctl -p /usr/sbin/smartctl -s [check]
```

# Options:
```
-p  [path]            Specifies the path to smartctl, default [/usr/sbin/smartctl]
-s  [check]           Check to be executed
    health_l          Check disk health data, individual disks
    health_s          Check disk health data, summary

-w [warning]         Warning count for Reallocated Sectors (default 1)
-c [critical]        Critical count for Reallocated Sectors (default 10)
-W [warning]         Warning percentage used for NVMe (default 90%)
-C [critical]        Critical percentage used for NVMe (default 95%)
```

# Examples:
```
./check_smartctl -s health_l	
./check_smartctl -s health_s -p /usr/sbin/smartctl
```
# Example Returns:
```
./check_smartctl -s health_s
"Number of Disks: 124 - Status: [OK]"
```