#START OF MAIN:

import configparser
from control import control
from roomalert_com import *
from mysql_write import *


def main():
    
    # Import Pump Monitor gonfiguration values from pm.cfg file in etc directory
    config = configparser.ConfigParser()
    config.read('/usr/local/pump-monitor/etc/pm.cfg') # Location of config file

    # Parse values into the main function.

    # Communication settings to connect to the Moxa E1242 module.
    SNMP_Host = config.get('COMMUNICATION SETTINGS','SNMP_Host')  # IP Address of the Moxa Module
    SNMP_Version = config.get('COMMUNICATION SETTINGS','SNMP_Version')  # SNMP Version
    SNMP_Community = config.get('COMMUNICATION SETTINGS','SNMP_Community') # SNMP Community String
    SNMP_Port = config.get('COMMUNICATION SETTINGS','SNMP_Port') # SNMP Port
    SNMP_Device = config.get('COMMUNICATION SETTINGS', 'SNMP_Device')  # SNMP Device

    # General settings for pump monitor program
    Cadance = config.getint('GENERAL MONITOR SETTINGS','Cadance')  # Monitor refresh rate in seconds
    Display = config.getboolean('GENERAL MONITOR SETTINGS','Display') # Enable Terminal Print
    SQL_Log = config.getboolean('GENERAL MONITOR SETTINGS','SQL_Log') # Enable BMS logging into SQL

    # Specific variables for the SQL database writer

    SQL_Host = config.get('MySQL SPECIFIC SETTINGS','SQL_Host')  # MySQL server address
    SQL_Auth = config.get('MySQL SPECIFIC SETTINGS','SQL_Auth')  # MySQL authentication method
    SQL_User = config.get('MySQL SPECIFIC SETTINGS','SQL_User')  # MySQl username
    SQL_Password = config.get('MySQL SPECIFIC SETTINGS','SQL_Password')  # MySQl user password
    SQL_Database = config.get('MySQL SPECIFIC SETTINGS','SQL_Database')  # MySQL database


    ################################################################################################################


    print('\nCurrent Configuration of Pump Monitor Program \n')
    print('Monitor Cadance: ' + str(Cadance))
    print('Control- Display:' +str(Display))
    print('Control- SQL Data Log:' + str(SQL_Log))
    print('\n')

    control(SNMP_Host=SNMP_Host, SNMP_Version=SNMP_Version, SNMP_Community=SNMP_Community, SNMP_Port=SNMP_Port, SNMP_Device=SNMP_Device, \
            Cadance=Cadance, Display=Display,SQL_Log=SQL_Log, \
            SQL_Host=SQL_Host, SQL_Auth=SQL_Auth, SQL_User=SQL_User,SQL_Password=SQL_Password,SQL_Database=SQL_Database)


if __name__ == '__main__':

    main()


