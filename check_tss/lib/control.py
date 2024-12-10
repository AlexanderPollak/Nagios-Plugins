# This script connects to Avtech RoomAlert 32S, reads temperature sensor values
# and sends shutdown commands to specified hosts in case the temperature value exceeds a threshold.


from avtech_com import *
import subprocess
import numpy as np


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
                                 "-H", str(NRPE_HOST), "-p", str(NRPE_PORT), "-c", str(NRPE_COMMAND), "-t", "2"],
                                capture_output=True,  # Capture stdout and stderr
                                text=True  # Decode output to strings
                                )

        # Get the return code and string
        return_code = int(result.returncode)
        return_string = str(result.stdout)

        # Print the script's output
        #print("Script Output:")
        #print(result.stdout)

        return [return_string, return_code]

    except:
        return [str("Error executing check_nrpe!"), int(2)]


def check_shutdown_condition(AVTECH, T_Sensor_C_1, T_Sensor_C_2, T_Sensor_C_3, N_Sensors, Shutdown_Temperature):
    """function to check if the temperature meets the shutdown condition. In case of a sensor failure it reduces
        the number of required sensors to the number of available sensors in case the specified sensor number
        exceeds the available sensors.

    Args:
        AVTECH:                 Object of the AVTECH roomalert unit.
        T_Sensor_C_1:           Temperature sensor 1 identifier.
        T_Sensor_C_2:           Temperature sensor 2 identifier.
        T_Sensor_C_3:           Temperature sensor 3 identifier.
        N_Sensors:              Number os temperature sensors that need to be above the threshold to trigger a shutdown.
        Shutdown_Temperature:   Threshold for the shutdown temperature.


    Returns: Boolean value True or False or None

    """

    try:

        # lists to track the sensor status
        sensor_val = [np.float64(999.0)] * 3
        sensor_ok = [None] * 3
        sensor_trig = [None] * 3

        if N_Sensors < 1 or N_Sensors > 3:
            print("Number of sensors specified in N_Sensors is outside the allowed range of 1-3")
            return None

        # Check that all sensors are connected and return a value
        tmp1 = AVTECH.read_di_temp_c(T_Sensor_C_1)
        tmp2 = AVTECH.read_di_temp_c(T_Sensor_C_2)
        tmp3 = AVTECH.read_di_temp_c(T_Sensor_C_3)
        sensor_val = [tmp1, tmp2, tmp3]
        # sensor list if the sensor is OK
        for sensor in range(len(sensor_val)):
            if sensor_val[sensor] == 999.0:
                sensor_ok[sensor] = False
            else:
                sensor_ok[sensor] = True

        # Checks each working sensor if it is above the threshold
        for sensor in range(len(sensor_ok)):
            if sensor_ok[sensor] == True and sensor_val[sensor] > np.float64(Shutdown_Temperature):
                sensor_trig[sensor] = True
            else:
                sensor_trig[sensor] = False

        # Get number of not working sensors and subtracting it from list of sensors to be checked
        # the lowest number is 1, hence if all sensors fail it still requires 1
        # basically checks if number of sensors required to pass is available if not it reduces the number
        # and adjusts it to the number of available sensors.
        if sensor_ok.count(False) > 0 and N_Sensors > sensor_ok.count(True):
            N_Sensors = max(N_Sensors - sensor_ok.count(False), 1)

        # checks if the specified number of sensors is triggered
        if sensor_trig.count(True) >= N_Sensors:
            return True
        else:
            return False

    except:
        print("Shutdown Condition Check failed")
        return None






def control(SNMP_Host, SNMP_Version, SNMP_Community, SNMP_Port, SNMP_Device, T_Sensor_C_1, T_Sensor_C_2, T_Sensor_C_3,
            N_Sensors, Shutdown_Temperature, Host_Names_Level_1):


    # nagios return values
    STATE_OK = 0
    STATE_WARNING = 1
    STATE_CRITICAL = 2
    STATE_UNKNOWN = 3
    STATE_DEPENDENT = 4

    NAGIOS_RETURN = STATE_UNKNOWN
    try:

        # ---------------------------------------------------------------------------#
        # Establish communication to Avtech RoomAlert 32S
        AVTECH = RA32S()
        AVTECH.open(SNMP_VERSION=SNMP_Version, SNMP_COMMUNITY=SNMP_Community, SNMP_HOST=SNMP_Host, SNMP_PORT=SNMP_Port,
                    SNMP_DEVICE=SNMP_Device)

        # Checks if connection to RoomAlert is successful
        tmp_a = AVTECH.is_connected()
        #print('Avtech Connection Established:' + str(tmp_a))
        if tmp_a == False:
            print("CRITICAL - No connection to Avtech Roomalert")
            return STATE_CRITICAL

        # Check if a shutdown condition is met!
        shutdown_required = check_shutdown_condition(AVTECH=AVTECH, T_Sensor_C_1=T_Sensor_C_1,
                                                     T_Sensor_C_2=T_Sensor_C_2, T_Sensor_C_3=T_Sensor_C_3,
                                                     N_Sensors=N_Sensors, Shutdown_Temperature=Shutdown_Temperature)


        # if shutdown required execute command on all servers
        #print('Shutdown Condition Check:' + str(shutdown_required))
        if not shutdown_required:
            print("OK - No Emergency Shutdown Required")
            return STATE_OK
        elif shutdown_required:
            for server in range(len(Host_Names_Level_1)):
                execute_nrpe(Host_Names_Level_1[server], "emergency_shutdown")
            print("CRITICAL - Emergency Shutdown Executed")
            return STATE_CRITICAL
        else:
            print("UNKNOWN - Shutdown Condition Check Failed!")
            return STATE_UNKNOWN


    except KeyboardInterrupt:
        try:
            del AVTECH
            print("UNKNOWN - Shutdown Condition Check Failed, Keyboard Interrupt!")
            return STATE_UNKNOWN
        except:
            print("UNKNOWN - Shutdown Condition Check Failed, Keyboard Interrupt!")
            return STATE_UNKNOWN

    except Exception as tmp_exeption:
        try:
            del AVTECH
            print("UNKNOWN - Shutdown Condition Check Failed, Exception: " + tmp_exeption)
            return STATE_UNKNOWN
        except:
            print("UNKNOWN - Shutdown Condition Check Failed, Exception: " + tmp_exeption)
            return STATE_UNKNOWN
