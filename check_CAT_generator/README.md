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

```


# Usage:
```

```

