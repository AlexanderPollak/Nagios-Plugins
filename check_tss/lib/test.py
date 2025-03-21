
from pysnmp.hlapi import *

iterator = getCmd(
    SnmpEngine(),
    CommunityData('public', mpModel=0),
    UdpTransportTarget(('10.2.3.15', 161)),
    ContextData(),
    ObjectType(ObjectIdentity('ROOMALERT32S-MIB', 'digital-sen2-1', 0))
)

errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

if errorIndication:
    print(errorIndication)

elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))

        varBinds[0].prettyPrint()
        t = str(varBinds[0].prettyPrint())

        t.partition("= ")[2]


