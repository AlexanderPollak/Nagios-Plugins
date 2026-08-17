# Check CAT Generator
Nagios script to check Catapiller Generator and log data into a mySQL database.: tested with D300 GC


# Requirements:
```
Python 3.10 or newer.

Network access to the Moxa NPort IA5150A IP address and TCP port.

Moxa configured in TCP Server mode with RS-485 at 115200 baud, 8 data bits, no parity, and 1 stop bit.

Generator Modbus slave ID set to 10.

Software must send Modbus RTU frames with CRC over the Moxa TCP connection.

Register values are signed 16-bit integers unless otherwise documented.

Apply the correct register offset; displayed register 1026 normally corresponds to protocol address 1025.

Only one application should access the Moxa serial connection at a time.
```

# Supported Devices
```
Catapiller Generator
		1. D300 GC

```

# Communication
```
Generator:The communication is established using Modbus RTU over a TCP connection provided by the Moxa NPort IA5150A.
The Moxa is connected via Ethernet to the control computer and acts as a transparent media converter to the generator’s RS-485 interface.
The serial connection operates at 115200,8,n,1, and the generator uses Modbus slave ID 10. The Python software must send complete Modbus RTU frames,
including the CRC, through the Moxa TCP port to read the generator’s signed 16-bit registers.
```



# CLASS Implementation


## generator_check: D300GC
```
This module contains classes and functions to communicate with the D300GC generator controller through the Moxa NPort IA5150A.

The class in this module ("D300GC") reads the generator’s Modbus registers and provides Nagios-compatible checks. Each check returns an OK, WARNING, CRITICAL, or UNKNOWN state.

List of monitored values:
1. Communication status
2. Generator operating state
3. Engine speed
4. Oil pressure
5. Coolant temperature
6. Starter-battery voltage
7. Fuel level
8. Generator output voltage
9. Generator output frequency
10. Generator output current
11. Engine operating hours
12. Active alarms and shutdowns

List of Nagios checks:
1. check_communication
2. check_operating_state
3. check_engine_speed
4. check_oil_pressure
5. check_coolant_temperature
6. check_battery_voltage
7. check_fuel_level
8. check_output_voltage
9. check_output_frequency
10. check_output_current
11. check_active_alarms
12. check_generator_status

List of functions:
    initialise()
    open()
    close()
    is_connected()
    read_register()
    read_generator_data()
    read_active_alarms()
    check_communication()
    check_operating_state()
    check_engine_speed()
    check_oil_pressure()
    check_coolant_temperature()
    check_battery_voltage()
    check_fuel_level()
    check_output_voltage()
    check_output_frequency()
    check_output_current()
    check_active_alarms()
    check_generator_status()
    log_generator_data()
```




## mysql_write: MySQL_com
```
This module contains classes and functions to write D300GC generator data into a MySQL database so that it can later be displayed and monitored using Grafana.

The class in this module ("mysql_com") manages the database connection and populates the generator-specific tables with timestamped measurements,
operating states, and alarm information.

List of stored values:
1. Generator operating state
2. Engine speed
3. Oil pressure
4. Coolant temperature
5. Starter-battery voltage
6. Fuel level
7. Output voltage
8. Output frequency
9. Output current
10. Engine operating hours
11. Active alarms and shutdowns
12. Communication status

List of functions:
    open()
    close()
    is_connected()
    write_D300GC()
```

# MySQL Database Tables
```
This section describes the MySQL table used to store D300GC generator measurements, operating status, and alarms for display in Grafana.

D300GC Generator Table:

DROP TABLE IF EXISTS `hcro_d300gc_generator`;

CREATE TABLE `hcro_d300gc_generator` (
    `ts`                          datetime(3) NOT NULL,
    `generator`                   varchar(16) NOT NULL,

    `communication_status`        varchar(16) DEFAULT NULL,
    `overall_status`              varchar(16) DEFAULT NULL,
    `control_mode_code`           smallint unsigned DEFAULT NULL,
    `control_mode`                varchar(64) DEFAULT NULL,
    `auto_start_enabled`          boolean DEFAULT NULL,
    `engine_state_code`           smallint unsigned DEFAULT NULL,
    `engine_state`                varchar(32) DEFAULT NULL,

    `oil_pressure_kpa`            smallint unsigned DEFAULT NULL,
    `coolant_temperature_c`       smallint DEFAULT NULL,
    `oil_temperature_c`           smallint DEFAULT NULL,
    `fuel_level_pct`              smallint unsigned DEFAULT NULL,
    `charge_alternator_voltage_v` decimal(4,1) DEFAULT NULL,
    `battery_voltage_v`           decimal(4,1) DEFAULT NULL,
    `engine_speed_rpm`            smallint unsigned DEFAULT NULL,

    `generator_frequency_hz`      decimal(4,1) DEFAULT NULL,
    `generator_l1_n_voltage_v`    decimal(8,1) DEFAULT NULL,
    `generator_l2_n_voltage_v`    decimal(8,1) DEFAULT NULL,
    `generator_l3_n_voltage_v`    decimal(8,1) DEFAULT NULL,
    `generator_l1_current_a`      decimal(7,1) DEFAULT NULL,
    `generator_l2_current_a`      decimal(7,1) DEFAULT NULL,
    `generator_l3_current_a`      decimal(7,1) DEFAULT NULL,
    `generator_total_power_w`     int DEFAULT NULL,
    `generator_power_factor`      decimal(4,2) DEFAULT NULL,

    `engine_run_time_s`           int unsigned DEFAULT NULL,
    `number_of_starts`            int unsigned DEFAULT NULL,
    `generator_positive_kwh`      decimal(11,1) DEFAULT NULL,

    `active_alarm_count`          smallint unsigned DEFAULT NULL,
    `active_alarms`               json DEFAULT NULL,

    PRIMARY KEY (`ts`, `generator`),
    KEY `idx_generator_ts` (`generator`, `ts`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```


# Software Installation
```
It is recommended to install the generator monitor in:

    /usr/local/check_CAT_generator/

Install the required Python modules:

    python3 -m pip install -r /usr/local/check_CAT_generator/etc/check_CAT_generator_pip_req.txt

Make the Nagios plugin executable:

    chmod 755 /usr/local/check_CAT_generator/check_CAT_generator.py

The MySQL account configured in `etc/check_CAT_generator.cfg` must have SELECT
permission on the generator table. The Nagios user must be able to execute the
plugin and read the configuration file. Because the configuration file contains
database credentials, do not make it world-readable.
```


# Usage:
```
./check_CAT_generator.py [check] [options]

Checks:

    control_mode   Check the controller mode and whether automatic start is enabled.
    autostart      Alias for control_mode.
    fuel_level     Check that the fuel level is at or above its threshold.
    active_alarms  Check whether the generator currently has active alarms.
    communication Check generator communication and database-data freshness.
    all            Run all four checks and return the most severe result.

Options:

    --config [path]          Configuration file. The default is
                             etc/check_CAT_generator.cfg relative to the plugin.
    --generator [name]       Generator name stored in MySQL. The default is
                             Generator_Type from the configuration file.
    --fuel-threshold [%]     Minimum acceptable fuel level. Default: 25%.
    --max-age [seconds]      Maximum age of the newest database row. The default
                             is twice the configured Cadance.
```


# How the Nagios Plugin Works
```
check_CAT_generator.py reads the newest row written to MySQL by the generator
monitor. It does not open another Modbus connection to the generator. This
prevents the Nagios check and the monitor from competing for the Moxa serial
connection.

The plugin selects the newest row for Generator_Type from
etc/check_CAT_generator.cfg. A different database generator name can be selected
with --generator.

The communication check uses both communication_status and the age of the newest
database row. The monitor only writes a complete row after a successful generator
read, so stale data also detects a stopped monitor, a failed database write, or a
generator communication failure. By default, the maximum age is twice Cadance
from check_CAT_generator.cfg. With the supplied Cadance of 60 seconds, the
default maximum age is 120 seconds.

Nagios return codes:

    0  OK
    1  WARNING
    2  CRITICAL
    3  UNKNOWN

Database connection errors, missing rows, invalid values, and unavailable values
return UNKNOWN. Disabled automatic start, fuel below its threshold, active
alarms, disconnected communication, and stale data return CRITICAL.
```


# Examples:
```
Check that the generator is in an automatic-start control mode:

    ./check_CAT_generator.py control_mode

Check the fuel level using a 30% minimum threshold:

    ./check_CAT_generator.py fuel_level --fuel-threshold 30

Check for active alarms:

    ./check_CAT_generator.py active_alarms

Check communication and require a database update within 180 seconds:

    ./check_CAT_generator.py communication --max-age 180

Run all checks together:

    ./check_CAT_generator.py all --fuel-threshold 30 --max-age 180
```


# Active Alarm Handling
```
generator_com.py reads the alarm map implemented by the controller and writes
the active alarm name and condition to the active_alarms JSON column. The Nagios
plugin reports active conditions only:

    warning
    shutdown
    electrical trip
    controlled shutdown
    active indication

Examples of supported alarm names include:

    Emergency stop
    Low oil pressure
    High coolant temperature
    Under speed
    Over speed
    Generator under frequency
    Generator over frequency
    Generator low voltage
    Generator high voltage
    Battery low voltage
    Charge alternator failure
    Fail to start
    Fail to stop
    Generator high current
    Low fuel level
    CAN ECU warning
    CAN ECU shutdown
    CAN ECU data failure

The exact list depends on whether the controller exposes the legacy page 8 alarm
map or the family-specific page 154 alarm map. Unknown implemented entries are
reported as "Alarm N" instead of being discarded.

The database stores every active alarm returned by generator_com.py. To keep the
single Nagios output line manageable, check_CAT_generator.py displays the first
five active alarms and then appends "+N more" when additional alarms are active.
```


# Example Returns:
```
./check_CAT_generator.py control_mode
"OK - control mode=Auto mode, auto-start is enabled"

./check_CAT_generator.py control_mode
"CRITICAL - control mode=Manual mode, auto-start is disabled"

./check_CAT_generator.py fuel_level --fuel-threshold 25
"OK - fuel level 68% is at or above the 25% threshold | fuel_level=68%;;25;0;100"

./check_CAT_generator.py active_alarms
"OK - no active alarms | active_alarms=0;;;0;"

./check_CAT_generator.py active_alarms
"CRITICAL - 2 active alarm(s): Low oil pressure (warning), High coolant temperature (shutdown) | active_alarms=2;;;0;"

./check_CAT_generator.py communication --max-age 120
"OK - generator communication is connected and database data is fresh (42s old) | data_age=42s;;120;0;"

./check_CAT_generator.py communication --max-age 120
"CRITICAL - database data is stale (300s old, maximum 120s); last communication status=CONNECTED | data_age=300s;;120;0;"
```


# Nagios Core Implementation
```
Copy or link the executable plugin into the Nagios plugin directory. The common
location is /usr/local/nagios/libexec, represented by $USER1$ in Nagios command
definitions. Keep the monitor configuration in
/usr/local/check_CAT_generator/etc/check_CAT_generator.cfg.

Add these command definitions to the Nagios commands configuration:

define command {
    command_name    check_cat_generator_control_mode
    command_line    $USER1$/check_CAT_generator.py control_mode --config /usr/local/check_CAT_generator/etc/check_CAT_generator.cfg
}

define command {
    command_name    check_cat_generator_fuel
    command_line    $USER1$/check_CAT_generator.py fuel_level --config /usr/local/check_CAT_generator/etc/check_CAT_generator.cfg --fuel-threshold $ARG1$
}

define command {
    command_name    check_cat_generator_alarms
    command_line    $USER1$/check_CAT_generator.py active_alarms --config /usr/local/check_CAT_generator/etc/check_CAT_generator.cfg
}

define command {
    command_name    check_cat_generator_communication
    command_line    $USER1$/check_CAT_generator.py communication --config /usr/local/check_CAT_generator/etc/check_CAT_generator.cfg --max-age $ARG1$
}

define command {
    command_name    check_cat_generator_all
    command_line    $USER1$/check_CAT_generator.py all --config /usr/local/check_CAT_generator/etc/check_CAT_generator.cfg --fuel-threshold $ARG1$ --max-age $ARG2$
}

Add service definitions to the generator host. Replace cat-generator with the
host_name already defined in the local Nagios configuration:

define service {
    use                     generic-service
    host_name               cat-generator
    service_description     CAT Generator Automatic Start
    check_command           check_cat_generator_control_mode
}

define service {
    use                     generic-service
    host_name               cat-generator
    service_description     CAT Generator Fuel Level
    check_command           check_cat_generator_fuel!25
}

define service {
    use                     generic-service
    host_name               cat-generator
    service_description     CAT Generator Active Alarms
    check_command           check_cat_generator_alarms
}

define service {
    use                     generic-service
    host_name               cat-generator
    service_description     CAT Generator Communication and Data
    check_command           check_cat_generator_communication!120
}

Alternatively, use one combined service instead of the four services above:

define service {
    use                     generic-service
    host_name               cat-generator
    service_description     CAT Generator Status
    check_command           check_cat_generator_all!25!120
}

Before reloading Nagios, run the plugin as the Nagios service account and verify
the Nagios configuration. The exact service-account name and Nagios configuration
path depend on the Linux distribution.

```
