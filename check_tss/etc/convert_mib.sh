#!/bin/bash
# Bash wrapper around python script - to convert mib to pysnmp format



python3  ../lib/mibdump.py  --mib-source="file:///usr/local/lib/python3.10/dist-packages/pysnmp/smi/mibs" --destination-directory="/usr/local/lib/python3.10/dist-packages/pysnmp/smi/mibs" --destination-format=pysnmp  /usr/share/snmp/mibs/moxa-e1242-v1.2.mib
python3  ../lib/mibdump.py  --mib-source="file:///usr/local/lib/python3.10/dist-packages/pysnmp/smi/mibs" --destination-directory="/usr/local/pump-monitor/etc" --destination-format=pysnmp  /usr/share/snmp/mibs/moxa-e1242-v1.2.mib
