#!/bin/bash
# Bash wrapper around python script - to convert mib to pysnmp format



python3  ../lib/mibdump.py  --mib-source="file:///usr/local/lib/python3.10/dist-packages/pysnmp/smi/mibs" --destination-directory="/usr/local/lib/python3.10/dist-packages/pysnmp/smi/mibs" --destination-format=pysnmp  /usr/share/snmp/mibs/ROOMALERT32S.MIB
python3  ../lib/mibdump.py  --mib-source="file:///usr/local/lib/python3.10/dist-packages/pysnmp/smi/mibs" --destination-directory="/usr/local/Nagios-Plugins/check_tss/etc" --destination-format=pysnmp  /usr/share/snmp/mibs/ROOMALERT32S.MIB
