""" This module contains classes and functions to establish communication with the
 Moxa E1200 Remote I/O Server via SNMP.

**Description:**

    The communication is established over SNMP protocol using the Moxa E1242 v1.2 MIB.
    The device is accessed via ethernet by the control computer.
    The functions in this module will allow to read device information and input values via SNMP,
    thereby allowing it to monitor analog and digital input values of the Remote I/O Server.
    This package includes functions to communicate with following
    devices:
        1. Moxa E1242 Remote I/O Server
    The main class in this module ("moxa_com") allows the user to
    read input values of the E1242 device.

    Notes:

    Uses 'snmpget' to acquire data via SNMP v1 and v3.:
    # installs SNMP package:
    sudo apt-get install snmp
    # downloads common SNMP MIBs:
    sudo apt-get install snmp-mibs-downloader
    Note that "moxa-e1242-v1.2.mib" needs to be copied into "/usr/share/snmp/mibs/"
    Note that /etc/snmp/snmp.conf needs to be modified:
    nano /etc/snmp/snmp.conf
    change in the fourth line "#mibs" to "mibs ALL"

"""
import numpy as np
import time
from struct import *

from pysnmp.hlapi import *
from time import time

# EMBEDDING com CLASS ----------------------------------------------------





class E1242(object):
    """This class implements the SNMP connection functions """
    def __init__(self):
        ''' Constructor for this class. '''
        self._port = 0
        self._host = 0
        self._community = 0
        self._version = 0



    def __del__(self):
        ''' Destructor for this class. '''




    def open (self,SNMP_VERSION = 2,SNMP_COMMUNITY = 'read',SNMP_HOST = '192.168.0.216',SNMP_PORT = 161, SNMP_DEVICE = 'E1242'):
        """Stores prameter to connect to Moxa E1242 via SNMPv1

        Args:
            SNMP_VERSION: SNMP Version. Default='2'
            SNMP_COMMUNITY: SNMP Community String. Default='public'
            SNMP_HOST: IP Address of the Moxa Module. Default='192.168.0.216'
            SNMP_PORT: SNMP Port. Default='161'


        Returns: Null

        """
        self._port = SNMP_PORT
        self._host = SNMP_HOST
        self._community = SNMP_COMMUNITY
        self._version = SNMP_VERSION
        self._device = SNMP_DEVICE



    def is_connected(self):
        """This function checks if the connection to the Moxa E1242 Module is established
        and if it responds to a readout command. It requests the system description
        and checks for the correct device (E1242).

        Returns: Boolean value True or False

        return
        """

        iterator = getCmd(
            SnmpEngine(),
            CommunityData(self._community, mpModel=0),
            UdpTransportTarget((self._host, self._port)),
            ContextData(),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))
        )

        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication:
            print(errorIndication)

        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

        else:

            tmp = str(varBinds[0].prettyPrint())
            daq_dev_model = tmp.partition("= ")[2]

            # Check for correct model and return true or false
            if self._device == daq_dev_model:
                return True
            else:
                return False



    def read_ai(self,channel):
        """This function reads the analog input value of the Moxa E1242. Depending on how it is
        configures in the device it returns the 0-10V value or the 4-20mA value.
        It returns the scaled value as shown in the web interface as float.

        Note that if the there is an error with the readout it will return the value "-1.0"

        Returns: float {Analog Input Voltage [V] or Analog Input Current [mA]}
        """

        # the index in SNMP is +1 of the channel number, which means AI channel 0 is equal to index 1
        index = np.uint32(channel + 1)

        # check that the input of the function is within the boundary of 0 to 4, note that this is device specific to E1242
        Upper_limit = 3  # upper limit channel 3
        Lower_limit = 0  # Lower limit channel 0
        if not Lower_limit <= channel <= Upper_limit:
            print('ERROR: Channel number out of bound. Must be within 0 to 3!')
            return None

        iterator_0 = getCmd(
            SnmpEngine(),
            CommunityData(self._community, mpModel=0),
            UdpTransportTarget((self._host, self._port)),
            ContextData(),
            ObjectType(ObjectIdentity('MOXA-IO-E1242-MIB', 'aiEnable', index))
        )

        iterator_1 = getCmd(
            SnmpEngine(),
            CommunityData(self._community, mpModel=0),
            UdpTransportTarget((self._host, self._port)),
            ContextData(),
            ObjectType(ObjectIdentity('MOXA-IO-E1242-MIB', 'aiMode', index))
        )

        iterator_2 = getCmd(
            SnmpEngine(),
            CommunityData(self._community, mpModel=0),
            UdpTransportTarget((self._host, self._port)),
            ContextData(),
            ObjectType(ObjectIdentity('MOXA-IO-E1242-MIB', 'aiValueScaled', index))
        )


        errorIndication_0, errorStatus_0, errorIndex_0, varBinds_0 = next(iterator_0)
        errorIndication_1, errorStatus_1, errorIndex_1, varBinds_1 = next(iterator_1)
        errorIndication_2, errorStatus_2, errorIndex_2, varBinds_2 = next(iterator_2)

        # print any error message
        if errorIndication_0:
            print(errorIndication_0)
        elif errorIndication_1:
            print(errorIndication_1)
        elif errorIndication_2:
            print(errorIndication_2)
        elif errorStatus_0:
            print('%s at %s' % (errorStatus_0.prettyPrint(), errorIndex_0 and varBinds_0[int(errorIndex_0) - 1][0] or '?'))
        elif errorStatus_1:
            print('%s at %s' % (errorStatus_1.prettyPrint(), errorIndex_1 and varBinds_1[int(errorIndex_1) - 1][0] or '?'))
        elif errorStatus_2:
            print('%s at %s' % (errorStatus_2.prettyPrint(), errorIndex_2 and varBinds_2[int(errorIndex_2) - 1][0] or '?'))
        else:

            # Check that input channel is enabled
            tmp = str(varBinds_0[0].prettyPrint())
            daq_enabled = tmp.partition("= ")[2]
            #print(daq_enabled)

            if not daq_enabled:
                print('ERROR: Selected Channel is disabled!')
                return None

            # acquire scaled value from analog input channel
            tmp = str(varBinds_2[0].prettyPrint())
            daq_ai_value = tmp.partition("= ")[2]
            #print(daq_ai_value)

            return np.float64(str(daq_ai_value))




    def read_di(self,channel):
        """This function reads the digital input of the Moxa E1242.
        It returns the boolean value True and False depending on the status of the input.

        Note that a high input (voltage present) leads to True value and a low input
        no voltage present leads to a False value. When comparing to the web interface
        1 = True and 0 = False

        Returns: Boolean value True or False
        """

        # the index in SNMP is +1 of the channel number, which means AI channel 0 is equal to index 1
        index = np.uint32(channel + 1)

        # check that the input of the function is within the boundary of 0 to 4, note that this is device specific to E1242
        Upper_limit = 3  # upper limit channel 3
        Lower_limit = 0  # Lower limit channel 0
        if not Lower_limit <= channel <= Upper_limit:
            print('ERROR: Channel number out of bound. Must be within 0 to 3!')
            return None

        iterator_0 = getCmd(
            SnmpEngine(),
            CommunityData(self._community, mpModel=0),
            UdpTransportTarget((self._host, self._port)),
            ContextData(),
            ObjectType(ObjectIdentity('MOXA-IO-E1242-MIB', 'diStatus', index))
        )

        errorIndication_0, errorStatus_0, errorIndex_0, varBinds_0 = next(iterator_0)


        # print any error message
        if errorIndication_0:
            print(errorIndication_0)
        elif errorStatus_0:
            print('%s at %s' % (errorStatus_0.prettyPrint(), errorIndex_0 and varBinds_0[int(errorIndex_0) - 1][0] or '?'))
        else:


            # acquire boolean valuefrom digital input channel
            tmp = str(varBinds_0[0].prettyPrint())
            daq_di_value =np.int32(str(tmp.partition("= ")[2]))
            if daq_di_value == 1:
                return True
            elif daq_di_value == 0:
                return False
            else:
                return None






