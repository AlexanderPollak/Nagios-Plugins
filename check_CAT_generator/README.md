# Check CAT Generator

Monitor a Caterpillar D300 GC generator, store its readings in MySQL for
Grafana, and run Nagios checks against the latest database record.


# Requirements:
```
Python 3.10 or newer.

Install the packages pinned in `etc/check_CAT_generator_pip_req.txt`:

    pyserial==3.5
    mysql-connector-python==26.7.0

Network access to the Moxa NPort IA5150A IP address and TCP port.

Moxa configured in TCP Server mode with RS-485 at 115200 baud, 8 data bits, no parity, and 1 stop bit.

Generator Modbus slave ID set to 10.

Software must send Modbus RTU frames with CRC over the Moxa TCP connection.

Register signedness, width, and scaling follow the GenComm register map. The
implemented readings include signed and unsigned 16-bit and 32-bit values.

Apply the correct register offset; displayed register 1026 normally corresponds to protocol address 1025.

Only one application should access the Moxa serial connection at a time.
```

# Supported Devices
```
Caterpillar Generator
		1. D300 GC

```

# Communication
```
Communication uses Modbus RTU frames over a TCP connection provided by the
Moxa NPort IA5150A. The Moxa is connected via Ethernet to the monitoring host
and acts as a transparent converter to the generator controller's RS-485
interface.

The RS-485 side operates at 115200,8,N,1, and the generator uses Modbus slave
ID 10. The monitor sends complete Modbus RTU frames, including the CRC, through
the Moxa TCP data port.

This is TCP/IP transport, but it is not native Modbus TCP with an MBAP header.
`generator_com.py` currently uses pyserial's `serial_for_url()` with a
`socket://host:port` URL as its TCP transport, so `pyserial` remains a runtime
dependency. The standalone `test_transfer_tcp.py` diagnostic uses Python's
built-in socket library directly.
```



# CLASS Implementation


## generator_com: D300GC
```
This module contains classes and functions to communicate with the D300GC generator controller through the Moxa NPort IA5150A.

The `D300GC` class reads and decodes the generator's GenComm registers. Nagios
checks are implemented separately in `check_CAT_generator.py` and read the
latest stored MySQL row instead of opening another generator connection.

List of monitored values:
1. Communication status
2. Overall controller status
3. Control mode and automatic-start state
4. Engine operating state and speed
5. Oil pressure and temperatures
6. Starter-battery and charge-alternator voltage
7. Fuel level
8. Generator voltage, frequency, current, power, and power factor
9. Engine run time, number of starts, and generated energy
10. Active alarms and shutdowns
11. Transfer to generator status

Key public functions:
    initialise()
    open()
    close()
    reconnect()
    is_connected()
    register_address()
    read_register()
    read_generator_data()
    read_active_alarms()
    read_transfer_to_generator()
    read_transfer_status()

Individual `read_*` methods are also provided for every stored measurement.
```




## mysql_write: MySQL_com
```
This module contains classes and functions to write D300GC generator data into a MySQL database so that it can later be displayed and monitored using Grafana.

The `MySQL_com` class manages the database connection and populates the generator-specific table with timestamped measurements,
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
13. Transfer to generator status

List of functions:
    open()
    close()
    is_connected()
    write_generator()
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
    `transfer_to_generator`       boolean DEFAULT NULL,
    `transfer_status`             varchar(32) DEFAULT NULL,
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

For an existing table, apply the included migration once before restarting the
monitor:

    mysql -u root -p grafanadata < etc/add_transfer_status_columns.sql
```


# Software Installation
```
Install the complete check_CAT_generator folder in the Nagios plugin directory:

    /usr/local/nagios/libexec/check_CAT_generator/

Install the required Python modules:

    python3 -m pip install -r /usr/local/nagios/libexec/check_CAT_generator/etc/check_CAT_generator_pip_req.txt

Make the Nagios plugin executable:

    chmod 755 /usr/local/nagios/libexec/check_CAT_generator/check_CAT_generator.py

Make the monitor wrapper executable:

    chmod 755 /usr/local/nagios/libexec/check_CAT_generator/monitor_CAT_generator.sh

The wrapper currently starts `./lib/main.py` using a relative path, so start it
from the installation directory:

    cd /usr/local/nagios/libexec/check_CAT_generator
    ./monitor_CAT_generator.sh

The monitor's MySQL account needs INSERT permission on the generator table. The
Nagios check needs SELECT permission. If both use the same configured account,
that account needs both permissions. Applying schema migrations requires a
separate account with ALTER permission.

The Nagios user must be able to execute the plugin and read the configuration
file. Because the configuration file contains database credentials, do not make
it world-readable.
```


# Usage:
```
./check_CAT_generator.py [check] [options]

Checks:

    control_mode   Check the controller mode and whether automatic start is enabled.
    autostart      Alias for control_mode.
    fuel_level     Check the fuel level against warning and critical thresholds.
    transfer_status Check whether the load is transferred to generator supply.
    transfer       Alias for transfer_status.
    on_emergency_power Return CRITICAL when the load is on generator supply.
    active_alarms  Check whether the generator currently has active alarms.
    communication Check generator communication and database-data freshness.
    all            Run all five checks and return the most severe result.

Options:

    --config [path]          Configuration file. The default is
                             /usr/local/nagios/libexec/check_CAT_generator/etc/
                             check_CAT_generator.cfg.
    --generator [name]       Generator name stored in MySQL. The default is
                             Generator_Type from the configuration file.
    --fuel-warning [%]       Fuel warning threshold. Default: 70%.
    --fuel-critical [%]      Fuel critical threshold. Default: 25%.
    --max-age [seconds]      Maximum age of the newest database row. The default
                             is twice the configured Cadance.
```


# How the Nagios Plugin Works
```
check_CAT_generator.py reads the newest row written to MySQL by the generator
monitor. It does not open another Modbus connection to the generator. This
prevents the Nagios check and the monitor from competing for the generator's
Moxa TCP/RTU connection.

The plugin selects the newest row for Generator_Type from
/usr/local/nagios/libexec/check_CAT_generator/etc/check_CAT_generator.cfg. A
different database generator name can be selected with --generator. The
--config option can select a different configuration during development or
testing.

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
return UNKNOWN. Disabled automatic start, fuel below 25%, active alarms,
emergency-generator operation, disconnected communication, and stale data
return CRITICAL. Fuel below 70% but not below 25% returns WARNING. The standalone
`transfer_status` check returns WARNING when the load is transferred; the
`on_emergency_power` check and the combined `all` check return CRITICAL.
```


# Examples:
```
Check that the generator is in an automatic-start control mode:

    ./check_CAT_generator.py control_mode

Check the fuel level using the default 70% warning and 25% critical thresholds:

    ./check_CAT_generator.py fuel_level

Check the fuel level using custom thresholds:

    ./check_CAT_generator.py fuel_level --fuel-warning 60 --fuel-critical 20

Check for active alarms:

    ./check_CAT_generator.py active_alarms

Check communication and require a database update within 180 seconds:

    ./check_CAT_generator.py communication --max-age 180

Run all checks together:

    ./check_CAT_generator.py all --fuel-warning 70 --fuel-critical 25 --max-age 180

Check whether the load has transferred to generator supply:

    ./check_CAT_generator.py transfer_status

Alert when the load is running on emergency generator power:

    ./check_CAT_generator.py on_emergency_power
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

./check_CAT_generator.py fuel_level
"OK - fuel level 75% is at or above the 70% warning threshold | fuel_level=75%;70:;25:;0;100"

./check_CAT_generator.py fuel_level
"WARNING - fuel level 68% is below the 70% warning threshold | fuel_level=68%;70:;25:;0;100"

./check_CAT_generator.py fuel_level
"CRITICAL - fuel level 12% is below the 25% critical threshold | fuel_level=12%;70:;25:;0;100"

./check_CAT_generator.py transfer_status
"OK - load is not transferred to generator supply"

./check_CAT_generator.py transfer_status
"WARNING - load is transferred to generator supply"

./check_CAT_generator.py on_emergency_power
"OK - load is not on emergency generator power"

./check_CAT_generator.py on_emergency_power
"CRITICAL - load is on emergency generator power; utility power outage indicated"

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
Install the complete folder at:

    /usr/local/nagios/libexec/check_CAT_generator/

For Nagios Core installations under /usr/local/nagios, the
/usr/local/nagios/libexec directory is normally represented by $USER1$ in
Nagios command definitions. The resulting layout is:

    /usr/local/nagios/libexec/check_CAT_generator/check_CAT_generator.py
    /usr/local/nagios/libexec/check_CAT_generator/monitor_CAT_generator.sh
    /usr/local/nagios/libexec/check_CAT_generator/etc/check_CAT_generator.cfg
    /usr/local/nagios/libexec/check_CAT_generator/lib/

Add these command definitions to the Nagios commands configuration:

define command {
    command_name    check_cat_generator_control_mode
    command_line    $USER1$/check_CAT_generator/check_CAT_generator.py control_mode
}

define command {
    command_name    check_cat_generator_fuel
    command_line    $USER1$/check_CAT_generator/check_CAT_generator.py fuel_level --fuel-warning $ARG1$ --fuel-critical $ARG2$
}

define command {
    command_name    check_cat_generator_alarms
    command_line    $USER1$/check_CAT_generator/check_CAT_generator.py active_alarms
}

define command {
    command_name    check_cat_generator_transfer
    command_line    $USER1$/check_CAT_generator/check_CAT_generator.py transfer_status
}

define command {
    command_name    check_cat_generator_emergency_power
    command_line    $USER1$/check_CAT_generator/check_CAT_generator.py on_emergency_power
}

define command {
    command_name    check_cat_generator_communication
    command_line    $USER1$/check_CAT_generator/check_CAT_generator.py communication --max-age $ARG1$
}

define command {
    command_name    check_cat_generator_all
    command_line    $USER1$/check_CAT_generator/check_CAT_generator.py all --fuel-warning $ARG1$ --fuel-critical $ARG2$ --max-age $ARG3$
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
    check_command           check_cat_generator_fuel!70!25
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
    service_description     CAT Generator Load Transfer
    check_command           check_cat_generator_transfer
}

define service {
    use                     generic-service
    host_name               cat-generator
    service_description     CAT Generator Emergency Power
    check_command           check_cat_generator_emergency_power
}

The load-transfer service gives a WARNING and the emergency-power service gives
a CRITICAL for the same transfer state. Use only the emergency-power service if
you do not want both alerts.

define service {
    use                     generic-service
    host_name               cat-generator
    service_description     CAT Generator Communication and Data
    check_command           check_cat_generator_communication!120
}

Alternatively, use one combined service instead of the separate services. The
combined check includes control mode, fuel level, emergency power, active
alarms, and communication/data freshness:

define service {
    use                     generic-service
    host_name               cat-generator
    service_description     CAT Generator Status
    check_command           check_cat_generator_all!70!25!120
}

Before reloading Nagios, run the plugin as the Nagios service account and verify
the Nagios configuration. The exact service-account name and Nagios configuration
path depend on the Linux distribution.

```
