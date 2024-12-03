# This script connects to the Pylontech US2000B Plus
# and read the charge status, voltage, current, and temperature
# it stores the data in a .csv file with the actual date

from moxa_com import *
from mysql_write import *
import time




def control(SNMP_Host, SNMP_Version, SNMP_Community, SNMP_Port, SNMP_Device, Cadance, Display, SQL_Log, SQL_Host, SQL_Auth, SQL_User, SQL_Password, SQL_Database):




    try:

        print('PumpMonitor:1.0.0 ')

        # ---------------------------------------------------------------------------#
        # Establish communication to MOXA E1242
        MOXA = E1242()
        MOXA.open(SNMP_VERSION=SNMP_Version, SNMP_COMMUNITY=SNMP_Community, SNMP_HOST=SNMP_Host, SNMP_PORT=SNMP_Port, SNMP_DEVICE=SNMP_Device)
        tmp_b = MOXA.is_connected()
        print('MOXA Connection Established:' + str(tmp_b))
        # ---------------------------------------------------------------------------#

        # ---------------------------------------------------------------------------#
        # Connect to MySQL Server
        SQL= MySQL_com()
        SQL.open(HOST=SQL_Host,USER =SQL_User,PASSWORD=SQL_Password,DATABASE=SQL_Database,AUTH_PLUGIN=SQL_Auth)
        time.sleep(1)
        tmp_s = SQL.is_connected()
        print('SQL Server Connection Established:' + str(tmp_s))
        # ---------------------------------------------------------------------------#



        # ---------------------------------------------------------------------------#
        if not (tmp_b):  # Stopps program if connection has not been established.
            print('ERROR: No Connection to MOXA E1242')
            exit()
        if not (tmp_s):  # Stopps program if connection has not been established.
            print('ERROR: No Connection to SQL Server!')
            exit()
        # ---------------------------------------------------------------------------#



        # ---------------------------------------------------------------------------#
        try:  # Program Loop
            print('Start Monitoring Program!')
            time.sleep(1)
            while True:
                time.sleep(Cadance)

                try:
                    #Read digital inputs for Pumps and system Fault
                    Sys_Fault = MOXA.read_di(0)
                    Pump_Status_1 = MOXA.read_di(1)
                    Pump_Status_2 = MOXA.read_di(2)
                    Pump_Status_3 = MOXA.read_di(3)

                    #read analog input for waterlevel
                    Analog_Voltage_WL = MOXA.read_ai(1)

                    #Convert analog voltage to waterlevel in mm [ Y=mx+b ]
                    m=56.67
                    b=24.32
                    Waterlevel_mm = np.float64((Analog_Voltage_WL*m) + b)

                except Exception as error:
                    del MOXA
                    del SQL
                    print('Readout loop error!', error)




                if SQL_Log:
                    try:
                        # pack monitor information in list to hand over to SQL class to write into the database
                        tmp_lines =1
                        tmp_ps_list = [[0 for i in range(6)] for j in range(tmp_lines)]
                        for x in range(tmp_lines):
                            tmp_ps_list[x][0] = float(Waterlevel_mm/10.0)  # Water Level in cm
                            tmp_ps_list[x][1] = float(0.0)  # System Temperature
                            tmp_ps_list[x][2] = str(Pump_Status_1)   # Status Pump 1
                            tmp_ps_list[x][3] = str(Pump_Status_2)   # Status Pump 2
                            tmp_ps_list[x][4] = str(Pump_Status_3)  # Status Pump 3
                            tmp_ps_list[x][5] = str(Sys_Fault)  # System Fault

                        SQL.write_PS(PS_LIST=tmp_ps_list)
                    except Exception as error:
                        print("SQL_Log error:", error)


                if Display:  # Condition to print the Pump System Status and Water Level in terminal
                    try:

                        print('System Status Fault:' + str(Sys_Fault) + '\t' + 'Pump 1 Active:' + str(Pump_Status_1) + '\t' + 'Pump 2 Active:' + str(Pump_Status_2) + '\t' + \
                              'Pump 3 Active:' + str(Pump_Status_3) + '\t' + 'Water Level in [cm]:' + str(Waterlevel_mm / 10.0))
                    except Exception as error:
                        del MOXA
                        del SQL
                        print('Display Values loop error!', error)





        except Exception as error:
            print("An error occurred:", error)




        except KeyboardInterrupt:
            try:
                del MOXA
                del SQL
                print('interrupted!')
            except:
                print('Monitoring Stop!')
            # ---------------------------------------------------------------------------#







    except KeyboardInterrupt:
        try:
            del MOXA
            del SQL
        except:
            print('Monitoring Stop!')

    except Exception as tmp_exeption:
        try:
            del MOXA

            del SQL
        except:
            print('Monitoring Stop! Exception'+tmp_exeption)