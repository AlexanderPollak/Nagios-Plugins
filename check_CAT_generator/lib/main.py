#START OF MAIN:

import configparser
import json
import sys
import time
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
    NPort_IP = config.get('COMMUNICATION SETTINGS', 'NPort_IP').strip()  # Moxa NPort IP address
    NPort_Port = config.getint('COMMUNICATION SETTINGS', 'NPort_Port')  # Moxa NPort TCP Server data port
    NPort_URL = f"socket://{NPort_IP}:{NPort_Port}"
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


    try:
        while True:
            cycle_started = time.monotonic()

            try:
                # Collect complete generator readings in a list.
                generator_data = []
                generator = D300GC(
                    port=NPort_URL,
                    slave_id=Modbus_Address,
                    baudrate=Serial_Baudrate,
                    timeout=Serial_Timeout,
                    request_delay=Serial_Request_Delay,
                )

                try:
                    generator.open()
                    generator_data.append(generator.read_generator_data())
                finally:
                    generator.close()

                if Display:
                    print(json.dumps(generator_data, indent=2, sort_keys=True))

                if Write_SQL:
                    # Connect to MySQL, write the collected generator data, and
                    # close the connection even when an insert fails.
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
            except Exception as error:
                print(f"Generator recording cycle failed: {error}", file=sys.stderr)

            cycle_elapsed = time.monotonic() - cycle_started
            time.sleep(max(0.0, Cadance - cycle_elapsed))
    except KeyboardInterrupt:
        print("Generator recording stopped.", file=sys.stderr)

    return




if __name__ == '__main__':
    generator_data = main()
