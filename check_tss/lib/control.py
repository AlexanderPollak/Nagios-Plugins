# This script connects to Avtech RoomAlert 32S, reads temperature sensor values
# and sends shutdown commands to specified hosts in case the temperature value exceeds a threshold.


from avtech_com import *
import subprocess
import time


def execute_nrpe(NRPE_HOST, NRPE_COMMAND, NRPE_PATH='/usr/local/nagios/libexec', NRPE_PORT=5660):
    """function to execute nagios nrpe commands

    Args:
        NRPE_HOST:      Host IP or DNS name, where the command should be executed. Takes a list of names or IP addresses.
        NRPE_COMMAND:   defines the command that will be executed through NRPE on the client server.
        NRPE_PATH:      Path to the NRPE check executable. Default='/usr/local/nagios/libexec'
        NRPE_PORT:      NRPE Port. Default='5660'



    Returns: list [str {command output}, int {Nagios status}]

        # nagios return values
        STATE_OK=0
        STATE_WARNING=1
        STATE_CRITICAL=2
        STATE_UNKNOWN=3
        STATE_DEPENDENT=4

    """

    # Path to the check_nrpe script
    program_path = NRPE_PATH + "/check_nrpe"
    # Execute the shell script
    try:
        result = subprocess.run([program_path,
                                 "-H", str(NRPE_HOST), "-p", str(NRPE_PORT), "-c", str(NRPE_COMMAND)],
                                capture_output=True,  # Capture stdout and stderr
                                text=True  # Decode output to strings
                                )

        # Get the return code and string
        return_code = int(result.returncode)
        return_string = str(result.stdout)

        # Print the script's output
        # print("Script Output:")
        # print(result.stdout)

        return [return_string, return_code]

    except:
        return [str("Error executing check_nrpe!"), int(2)]


def check_shutdown_condition(AVTECH, T_Sensor_C_1, T_Sensor_C_2, T_Sensor_C_3, N_Sensors, Shutdown_Temperature):
    """function to check if the temperature meets the shutdown condition

    Args:
        AVTECH:                 Object of the AVTECH roomalert unit.
        T_Sensor_C_1:           Temperature sensor 1 identifier.
        T_Sensor_C_2:           Temperature sensor 2 identifier.
        T_Sensor_C_3:           Temperature sensor 3 identifier.
        N_Sensors:              Number os temperature sensors that need to be above the threshold to trigger a shutdown.
        Shutdown_Temperature:   Threshold for the shutdown temperature.


    Returns: Boolean value True or False

    """

    try:

        # lists to track the sensor status
        sensor_val = []
        sensor_ok = []
        sensor_trig = []

        if N_Sensors < 1 or N_Sensors > 3:
            print("Number of sensors specified in N_Sensors is outside the allowed range of 1-3")
            return

        # Check that all sensors are connected and return a value
        tmp1 = AVTECH.read_di_temp_c(T_Sensor_C_1)
        tmp2 = AVTECH.read_di_temp_c(T_Sensor_C_2)
        tmp3 = AVTECH.read_di_temp_c(T_Sensor_C_3)
        sensor_val = [tmp1, tmp2, tmp3]
        # sensor list if the sensor is OK
        for sensor in sensor_val:
            if sensor_val[sensor] == 999.0:
                sensor_ok[sensor] = False
            else:
                sensor_ok[sensor] = True

        # Checks each working sensor if it is above the threshold
        for sensor in sensor_ok:
            if sensor == True and sensor_val > Shutdown_Temperature:
                sensor_trig[sensor] = True
            else:
                sensor_trig[sensor] = False

        # checks if the specified number of sensors is triggered
        if sensor_trig.count(True) == N_Sensors:
            return True
        else:
            return False

    except:
        print("Shutdown Condition Check failed")





def control(SNMP_Host, SNMP_Version, SNMP_Community, SNMP_Port, SNMP_Device, T_Sensor_C_1, T_Sensor_C_2, T_Sensor_C_3,
            N_Sensors, Shutdown_Temperature, Shutdown_Message, Host_Names_Level_1):
    try:

        print('ThermalServerShutdown:1.0.0 ')

        # ---------------------------------------------------------------------------#
        # Establish communication to Avtech RoomAlert 32S
        AVTECH = RA32S()

        AVTECH.open(SNMP_VERSION=SNMP_Version, SNMP_COMMUNITY=SNMP_Community, SNMP_HOST=SNMP_Host, SNMP_PORT=SNMP_Port,
                    SNMP_DEVICE=SNMP_Device)

        tmp_a = AVTECH.is_connected()
        print('Avtech Connection Established:' + str(tmp_a))

        temp_check_passed = check_shutdown_condition(AVTECH=AVTECH, T_Sensor_C_1=T_Sensor_C_1,
                                                     T_Sensor_C_2=T_Sensor_C_2, T_Sensor_C_3=T_Sensor_C_3,
                                                     N_Sensors=N_Sensors, Shutdown_Temperature=Shutdown_Temperature)

        print('Shutdown Condition Check:' + str(temp_check_passed))

        # ---------------------------------------------------------------------------#




        # # ---------------------------------------------------------------------------#
        # if not (tmp_b):  # Stopps program if connection has not been established.
        #     print('ERROR: No Connection to MOXA E1242')
        #     exit()
        # if not (tmp_s):  # Stopps program if connection has not been established.
        #     print('ERROR: No Connection to SQL Server!')
        #     exit()
        # # ---------------------------------------------------------------------------#
        #
        #
        #
        # # ---------------------------------------------------------------------------#
        # try:  # Program Loop
        #     print('Start Monitoring Program!')
        #     time.sleep(1)
        #     while True:
        #         time.sleep(Cadance)
        #
        #         try:
        #             #Read digital inputs for Pumps and system Fault
        #             Sys_Fault = MOXA.read_di(0)
        #             Pump_Status_1 = MOXA.read_di(1)
        #             Pump_Status_2 = MOXA.read_di(2)
        #             Pump_Status_3 = MOXA.read_di(3)
        #
        #             #read analog input for waterlevel
        #             Analog_Voltage_WL = MOXA.read_ai(1)
        #
        #             #Convert analog voltage to waterlevel in mm [ Y=mx+b ]
        #             m=56.67
        #             b=24.32
        #             Waterlevel_mm = np.float64((Analog_Voltage_WL*m) + b)
        #
        #         except Exception as error:
        #             del MOXA
        #             del SQL
        #             print('Readout loop error!', error)
        #
        #
        #
        #
        #         if SQL_Log:
        #             try:
        #                 # pack monitor information in list to hand over to SQL class to write into the database
        #                 tmp_lines =1
        #                 tmp_ps_list = [[0 for i in range(6)] for j in range(tmp_lines)]
        #                 for x in range(tmp_lines):
        #                     tmp_ps_list[x][0] = float(Waterlevel_mm/10.0)  # Water Level in cm
        #                     tmp_ps_list[x][1] = float(0.0)  # System Temperature
        #                     tmp_ps_list[x][2] = str(Pump_Status_1)   # Status Pump 1
        #                     tmp_ps_list[x][3] = str(Pump_Status_2)   # Status Pump 2
        #                     tmp_ps_list[x][4] = str(Pump_Status_3)  # Status Pump 3
        #                     tmp_ps_list[x][5] = str(Sys_Fault)  # System Fault
        #
        #                 SQL.write_PS(PS_LIST=tmp_ps_list)
        #             except Exception as error:
        #                 print("SQL_Log error:", error)
        #
        #
        #         if Display:  # Condition to print the Pump System Status and Water Level in terminal
        #             try:
        #
        #                 print('System Status Fault:' + str(Sys_Fault) + '\t' + 'Pump 1 Active:' + str(Pump_Status_1) + '\t' + 'Pump 2 Active:' + str(Pump_Status_2) + '\t' + \
        #                       'Pump 3 Active:' + str(Pump_Status_3) + '\t' + 'Water Level in [cm]:' + str(Waterlevel_mm / 10.0))
        #             except Exception as error:
        #                 del MOXA
        #                 del SQL
        #                 print('Display Values loop error!', error)
        #
        #
        #
        #
        #
        # except Exception as error:
        #     print("An error occurred:", error)
        #
        #
        #
        #
        # except KeyboardInterrupt:
        #     try:
        #         del MOXA
        #         del SQL
        #         print('interrupted!')
        #     except:
        #         print('Monitoring Stop!')
        #     # ---------------------------------------------------------------------------#


    except KeyboardInterrupt:
        try:
            del AVTECH
            # del SQL
        except:
            print('Monitoring Stop!')

    except Exception as tmp_exeption:
        try:
            del AVTECH
            # del SQL
        except:
            print('Monitoring Stop! Exception' + tmp_exeption)
