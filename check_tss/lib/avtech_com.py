""" This module contains classes and functions to establish communication with the
 Avtech RoomAlert 32S Environmental Monitor via SNMP.

**Description:**

    The communication is established over SNMP protocol using the Avtech ROOMALERT32S MIB.
    The device is accessed via ethernet by the control computer.
    The functions in this module will allow to read device information and input values via SNMP,
    thereby allowing it to monitor digital input values of the RoomAlert unit.
    This package includes functions to communicate with following
    devices:
        1. Avtech RoomAlert 32S
    The main class in this module ("RA32S") allows the user to
    read input values of the RoomAlert 32S device.

    Notes:

    Uses 'snmpget' to acquire data via SNMP v1 and v3.:
    # installs SNMP package:
    sudo apt-get install snmp
    # downloads common SNMP MIBs:
    sudo apt-get install snmp-mibs-downloader
    Note that "ROOMALERT32S.MIB" needs to be copied into "/usr/share/snmp/mibs/"
    Note that /etc/snmp/snmp.conf needs to be modified:
    nano /etc/snmp/snmp.conf
    change in the fourth line "#mibs" to "mibs ALL"

"""
import numpy as np
from pysnmp.hlapi import *


# EMBEDDING com CLASS ----------------------------------------------------





class RA32S(object):
    """This class implements the SNMP connection functions """
    def __init__(self):
        ''' Constructor for this class. '''
        self._port = 0
        self._host = 0
        self._community = 0
        self._version = 0



    def __del__(self):
        ''' Destructor for this class. '''




    def open (self,SNMP_VERSION = 2,SNMP_COMMUNITY = 'public',SNMP_HOST = '10.2.3.15',SNMP_PORT = 161, SNMP_DEVICE = 'AVTECH RoomAlert 32S'):
        """Stores prameter to connect to RoomAlert 32S via SNMPv1

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
        """This function checks if the connection to the Avtech RoomAlert 32S unit is established
        and if it responds to a readout command. It requests the system description
        and checks for the correct device (AVTECH RoomAlert 32S).

        Returns: Boolean value True or False

        """
        try:
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
                #print(daq_dev_model)
                # Check for correct model and return true or false
                if self._device == daq_dev_model:
                    return True
                else:
                    return False
        except:
            return False



    def read_di_temp_c(self,channel):
        """This function reads the digital input temperature value from the connected temperature sensors
        of the Avtech RoomAlert 32S. This function requires a temperature sensor, or a temoerature & humidity sensor
        to be connected to the defined input channel. It only reads the temperature value register for deg C
        and returns a float [Celsius].

        Note that if the there is an error with the readout it will return a value of 999

        Returns: float {Temperature in [deg Celsius]}
        """


        iterator = getCmd(
            SnmpEngine(),
            CommunityData(self._community, mpModel=0),
            UdpTransportTarget((self._host, self._port)),
            ContextData(),
            ObjectType(ObjectIdentity("ROOMALERT32S-MIB", channel, 0))
        )



        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)


        # print any error message or return the queried value
        if errorIndication:
            print(errorIndication)
            return float(999)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            return float(999)
        else:
            # acquire temperature value and scale it to deg C
            tmp = str(varBinds[0].prettyPrint())
            tmp_temp_c= (np.float64(str(tmp.partition("= ")[2])))/100.0

            return tmp_temp_c

