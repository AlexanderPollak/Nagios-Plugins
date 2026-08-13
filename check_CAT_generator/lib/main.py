#START OF MAIN:

import configparser
import json
from pathlib import Path

from generator_com import D300GC
from mysql_write import MySQL_com




def main():
    
    # Import check_CAT_generator configuration values from check_CAT_generator.cfg file in etc directory
    config = configparser.ConfigParser()
    config_path = Path(__file__).resolve().parent.parent / 'etc' / 'check_CAT_generator.cfg'
    config.read(config_path)

    # Parse values into the control function.

    # Communication settings to connect to the CAT Generator
    Generator_Type = config.get('COMMUNICATION SETTINGS','Generator_Type')  # Generator Type
    Serial_Port = config.get('COMMUNICATION SETTINGS','Serial_Port')  # Serial Port for Communication with Moxa TCP/IP module at Generator
    Modbus_Address = config.getint('COMMUNICATION SETTINGS','Modbus_Address') # Modbus Address for Generator
    Serial_Baudrate = config.getint('COMMUNICATION SETTINGS', 'Serial_Baudrate')  # Serial baudrate for CAT communication
    Serial_Timeout = config.getfloat('COMMUNICATION SETTINGS', 'Serial_Timeout')  # Serial timeout for CAT communication
    Serial_Request_Delay = config.getfloat('COMMUNICATION SETTINGS', 'Serial_Request_Delay')  # Serial delay for CAT communication


    # General values for the check_CAT_generatror software
    Cadance = config.getint('GENERAL SETTINGS','Cadance')  # Database recording cadance [seconds]
    Display = config.getboolean('GENERAL SETTINGS', 'Display')  # Display the recorded data in the terminal [True / False]
    Write_SQL = config.getboolean('GENERAL SETTINGS','Write_SQL')  # Writes the recorded data in the SQL database [True / False]

    # Specific variables for the SQL database writer

    SQL_Host = config.get('MySQL SPECIFIC SETTINGS','SQL_Host')  # MySQL server address
    SQL_Auth = config.get('MySQL SPECIFIC SETTINGS','SQL_Auth')  # MySQL authentication method
    SQL_User = config.get('MySQL SPECIFIC SETTINGS','SQL_User')  # MySQl username
    SQL_Password = config.get('MySQL SPECIFIC SETTINGS','SQL_Password')  # MySQl user password
    SQL_Database = config.get('MySQL SPECIFIC SETTINGS','SQL_Database')  # MySQL database
    SQL_Table = config.get('MySQL SPECIFIC SETTINGS', 'SQL_Table')  # MySQL table in defined database.


    ################################################################################################################


    #print('Current Configuration of Control program Rev. 1.0.0 \n')
    #print('Cadance: ' + str(Cadance))
    #print('\n')


    # ---------------------------------------------------------------------------#
    # Collect complete generator readings in a list.
    generator_data = []
    generator = D300GC(port=Serial_Port, slave_id=Modbus_Address, baudrate=Serial_Baudrate, timeout=Serial_Timeout, request_delay=Serial_Request_Delay)

    try:
        generator.open()
        generator_data.append(generator.read_generator_data())
    finally:
        generator.close()

    if Display:
        print(json.dumps(generator_data, indent=2, sort_keys=True))

    # ---------------------------------------------------------------------------#
    if Write_SQL:
        # Connect to MySQL, write the collected generator data, and close the
        # connection even when an insert fails.
        sql = MySQL_com()
        sql_connected = False
        try:
            sql_connected = sql.open(HOST=SQL_Host,USER=SQL_User,PASSWORD=SQL_Password,DATABASE=SQL_Database,GENERATOR_TABLE=SQL_Table,AUTH_PLUGIN=SQL_Auth)
            if not sql_connected:
                raise ConnectionError("Unable to connect to the MySQL database")

            write_successful = sql.write_generator(
                generator_data=generator_data,
                generator_name=Generator_Type,
            )
            if not write_successful:
                raise RuntimeError("Failed to write generator data to MySQL")
        finally:
            if sql_connected:
                sql.close()

    return generator_data

#        # ---------------------------------------------------------------------------#
#        # Connect to MySQL Server
#        SQL= MySQL_com()
#        SQL.open(HOST=SQL_Host,USER =SQL_User,PASSWORD=SQL_Password,DATABASE=SQL_Database,AUTH_PLUGIN=SQL_Auth)
#        time.sleep(1)
#        tmp_s = SQL.is_connected()
#        print('SQL Server Connection Established:' + str(tmp_s))
#        # ---------------------------------------------------------------------------#

#if SQL_Log:
#    try:
#        SQL.write_BMS(BMS_LIST=tmp_bms_log)
#        SQL.write_XW(XW_LIST=tmp_xw_log)
#        SQL.write_MPPT(MPPT_LIST=tmp_mppt_log)
#    except Exception as error:
#        print("SQL_Log error:", error)


if __name__ == '__main__':
    generator_data = main()
