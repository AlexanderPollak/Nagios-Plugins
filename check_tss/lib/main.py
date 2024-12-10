#START OF MAIN:

import configparser
from control import control
import sys

def parse_repeated_keys(file_path, section_name, key_name):
    results = []
    with open(file_path, "r") as file:
        in_section = False
        for line in file:
            line = line.strip()
            if line.startswith(f"[{section_name}]"):
                in_section = True
                continue
            if in_section:
                if line.startswith("[") and line.endswith("]"):
                    break  # End of section
                if "=" in line:
                    key, value = line.split("=", 1)
                    if key.strip() == key_name:
                        results.append(value.strip())
    return results

def main():




    # Import Thermal Server Shutdown configuration values from tss.cfg file in etc directory
    config = configparser.ConfigParser(strict=False)
    file_path = '/usr/local/nagios/libexec/check_tss/etc/tss.cfg' # Location of config file
    config.read(file_path) # Load file path

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


    # Specific list of hosts that will be shutdown during an overheat event.
    Host_Names_Level_1 = parse_repeated_keys(file_path,'HOST LIST','Host_Names_Level_1')  # List of Hosts

    ################################################################################################################
    #print(Host_Names_Level_1)

    tmp_return=control(SNMP_Host=SNMP_Host, SNMP_Version=SNMP_Version, SNMP_Community=SNMP_Community, SNMP_Port=SNMP_Port, SNMP_Device=SNMP_Device, \
            T_Sensor_C_1=T_Sensor_C_1, T_Sensor_C_2=T_Sensor_C_2, T_Sensor_C_3=T_Sensor_C_3, \
            N_Sensors=N_Sensors, Shutdown_Temperature=Shutdown_Temperature, Host_Names_Level_1=Host_Names_Level_1)

    # returns the nagios information if Ok or NOK
    return tmp_return

if __name__ == '__main__':


    tmp_return = main()
    sys.exit(tmp_return)

