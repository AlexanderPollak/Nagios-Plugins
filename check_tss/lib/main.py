#START OF MAIN:

import configparser
from control import control
from avtech_com import *



def main():
    
    # Import Thermal Server Shutdown configuration values from tss.cfg file in etc directory
    config = configparser.ConfigParser()
    config.read('/usr/local/nagios/libexec/check_tss/etc/tss.cfg') # Location of config file

    # Parse values into the main function.

    # Communication settings to connect to the Avtech RoomAlert 32S module.
    SNMP_Host = config.get('COMMUNICATION SETTINGS','SNMP_Host')  # IP Address of the RoomAlert Module
    SNMP_Version = config.get('COMMUNICATION SETTINGS','SNMP_Version')  # SNMP Version
    SNMP_Community = config.get('COMMUNICATION SETTINGS','SNMP_Community') # SNMP Community String
    SNMP_Port = config.get('COMMUNICATION SETTINGS','SNMP_Port') # SNMP Port
    SNMP_Device = config.get('COMMUNICATION SETTINGS', 'SNMP_Device')  # SNMP Device

    # General settings to monitor specific temperature sensors connected to the RoomAlert Module.
    # 3 temperature sensors are required for this program and are defined by the MIB identifier.
    T_Sensor_C_1 = config.get('GENERAL MONITOR SETTINGS','T_Sensor_C_1')    # Temperature Sensor 1
    T_Sensor_C_2 = config.get('GENERAL MONITOR SETTINGS','T_Sensor_C_2')    # Temperature Sensor 2
    T_Sensor_C_3 = config.get('GENERAL MONITOR SETTINGS','T_Sensor_C_3')    # Temperature Sensor 3





    # Specific conditions to trigger a thermal server shutdown
    N_Sensors = config.getint('GENERAL CONTROL SETTINGS','N_Sensors')  # Number of sensors to trigger a shutdown
    Shutdown_Temperature = config.getint('GENERAL CONTROL SETTINGS', 'Shutdown_Temperature')  # Temperature threshold to trigger a shutdown
    Shutdown_Message = config.get('GENERAL CONTROL SETTINGS', 'Shutdown_Message')  # Shutdown message

    # Specific list of hosts that will be shutdown during an overheat event.
    Host_Names_Level_1 = config.get('HOST LIST', 'Host_Names_Level_1').split(", ")  # List of Hosts


    ################################################################################################################


    print('\nCurrent Configuration of Thermal Server Shutdown \n')
   # print('Monitor Cadance: ' + str(Cadance))
   # print('Control- Display:' +str(Display))
   # print('Control- SQL Data Log:' + str(SQL_Log))
   # print('\n')

    control(SNMP_Host=SNMP_Host, SNMP_Version=SNMP_Version, SNMP_Community=SNMP_Community, SNMP_Port=SNMP_Port, SNMP_Device=SNMP_Device, \
            T_Sensor_C_1=T_Sensor_C_1, T_Sensor_C_2=T_Sensor_C_2, T_Sensor_C_3=T_Sensor_C_3, \
            N_Sensors=N_Sensors, Shutdown_Temperature=Shutdown_Temperature, Shutdown_Message=Shutdown_Message, Host_Names_Level_1=Host_Names_Level_1)


if __name__ == '__main__':

    main()


