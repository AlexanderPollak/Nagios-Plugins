"""MySQL storage support for CAT D300GC generator data.

The :class:`MySQL_com` class manages the connection to a MySQL database and
writes the complete data returned by ``D300GC.read_generator_data()`` into the
``hcro_d300gc_generator`` table. Each stored row includes a timestamp and
generator name together with operating mode, engine status, instrumentation,
accumulated values, and active alarms. Active alarms are serialized as JSON for
storage in the table's JSON column.

The database connection requires a valid host, username, password, database
name, and authentication method. Generator readings can be passed to
``write_generator()`` as either one dictionary or the list of dictionaries
collected by ``main.py``.
"""
import datetime
import json
import re

import mysql.connector
#import logging


# EMBEDDING Pylontech CLASS ----------------------------------------------------

class MySQL_com():
    """Manage the MySQL connection and write D300GC generator readings."""

    GENERATOR_DATA_COLUMNS = (
        "communication_status",
        "overall_status",
        "control_mode_code",
        "control_mode",
        "auto_start_enabled",
        "engine_state_code",
        "engine_state",
        "oil_pressure_kpa",
        "coolant_temperature_c",
        "oil_temperature_c",
        "fuel_level_pct",
        "charge_alternator_voltage_v",
        "battery_voltage_v",
        "engine_speed_rpm",
        "generator_frequency_hz",
        "generator_l1_n_voltage_v",
        "generator_l2_n_voltage_v",
        "generator_l3_n_voltage_v",
        "generator_l1_current_a",
        "generator_l2_current_a",
        "generator_l3_current_a",
        "generator_total_power_w",
        "generator_power_factor",
        "engine_run_time_s",
        "number_of_starts",
        "generator_positive_kwh",
        "active_alarm_count",
        "active_alarms",
    )

    def __init__(self):
        ''' Constructor for this class. '''
        self._port = 0
        self._generator_table = None


    def __del__(self):
        ''' Destructor for this class. '''
        try:
            if self._port != 0:
                self.close()
        except Exception:
            # Destructors must never emit errors during interpreter shutdown.
            pass

    def open (self,HOST,USER ,PASSWORD,DATABASE, GENERATOR_TABLE,AUTH_PLUGIN = "mysql_native_password"):
        """Establishing the connection to the mqsql database

        Args:
            HOST: network address of the server hosting the mysql database.
            USER: mysql database user login for specified database.
            PASSWORD: mysql database user password for specified user.
            DATABASE: specifies the mysql database.
            GENERATOR_TABLE: specifies the mysql table name.
            AUTH_PLUGIN: specifies the login method to the mysql server. Default='mysql_native_password'

        Returns: Boolean value True or False

        """
        if not isinstance(GENERATOR_TABLE, str) or not re.fullmatch(
            r"[A-Za-z_][A-Za-z0-9_]*", GENERATOR_TABLE
        ):
            raise ValueError("GENERATOR_TABLE must be a valid MySQL identifier")

        self._generator_table = GENERATOR_TABLE
        self._port = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE, auth_plugin=AUTH_PLUGIN)
        if not self._port.is_connected():
            print("Unable to connect to " + str(HOST))

        return self._port.is_connected()

    def close(self):
        """Closes the connection to the MySQL server

        Returns: Boolean value True or False

        """
        self._port.close()
        return not self._port.is_connected()

    def is_connected(self):
        """This function checks if the connection to the MySQL server is established.


        Returns: Boolean value True or False

        """
        return self._port.is_connected()

    def write_generator(
        self,
        generator_data,
        generator_name="D300GC",
        timestamp=None,
    ):
        """Write data returned by ``D300GC.read_generator_data()``.

        ``generator_data`` may be either one readout dictionary or the list of
        dictionaries collected by ``main.py``. The database timestamp and
        generator name are supplied here because they are not Modbus values.
        A record may optionally contain its own ``ts`` and ``generator`` keys,
        which take precedence over the method arguments.

        Returns ``True`` after a successful commit and ``False`` after a MySQL
        error. Invalid input raises ``TypeError`` or ``ValueError`` before any
        database operation is attempted.
        """
        if isinstance(generator_data, dict):
            records = [generator_data]
        elif isinstance(generator_data, (list, tuple)):
            records = list(generator_data)
        else:
            raise TypeError("generator_data must be a dictionary or a list of dictionaries")

        if not records:
            raise ValueError("generator_data must contain at least one reading")
        if not isinstance(generator_name, str) or not generator_name:
            raise ValueError("generator_name must be a non-empty string")
        if len(generator_name) > 16:
            raise ValueError("generator_name must not exceed 16 characters")
        if self._port == 0 or not self._port.is_connected():
            raise RuntimeError("MySQL connection is not open")
        if self._generator_table is None:
            raise RuntimeError("MySQL generator table is not configured")

        columns = ("ts", "generator") + self.GENERATOR_DATA_COLUMNS
        quoted_columns = ", ".join("`{}`".format(column) for column in columns)
        placeholders = ", ".join(["%s"] * len(columns))
        sql = "INSERT INTO `{}` ({}) VALUES ({})".format(
            self._generator_table,
            quoted_columns,
            placeholders,
        )

        default_timestamp = timestamp or datetime.datetime.now()
        values = []
        for record_number, record in enumerate(records, start=1):
            if not isinstance(record, dict):
                raise TypeError(
                    "generator_data record {} must be a dictionary".format(
                        record_number
                    )
                )

            missing = [
                column
                for column in self.GENERATOR_DATA_COLUMNS
                if column not in record
            ]
            if missing:
                raise ValueError(
                    "generator_data record {} is missing fields: {}".format(
                        record_number,
                        ", ".join(missing),
                    )
                )

            record_timestamp = record.get("ts", default_timestamp)
            record_generator = record.get("generator", generator_name)
            if not isinstance(record_generator, str) or not record_generator:
                raise ValueError("generator must be a non-empty string")
            if len(record_generator) > 16:
                raise ValueError("generator must not exceed 16 characters")

            active_alarms = record["active_alarms"]
            if active_alarms is not None:
                active_alarms = json.dumps(active_alarms, sort_keys=True)

            row = [record_timestamp, record_generator]
            for column in self.GENERATOR_DATA_COLUMNS:
                value = active_alarms if column == "active_alarms" else record[column]
                row.append(value)
            values.append(tuple(row))

        cursor = self._port.cursor()
        try:
            cursor.executemany(sql, values)
            self._port.commit()
            return True
        except mysql.connector.Error as error:
            self._port.rollback()
            print("Failed to write generator data to database: {}".format(error))
            return False
        finally:
            cursor.close()



