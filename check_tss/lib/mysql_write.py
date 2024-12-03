""" This module contains classes and functions to write Pylontech battery,
Schneider XW+ 8548E, and Schneider MPPT60 150 data into a mysql data base.  

**Description:**

    This module contains a description for each table in the data base and the implementation two write 
    data into the specific tables. It requires a valid username, password, hostaddress, and database.
    This package includes functions to write aquired data from the following devices:
        1. Pylontech US2000B Battery
        2. Schneider MPPT60 150
        3. Schneider XW+ 8548E

The class in this module ("mysql_com") allows the user to
communicate with the mysql database. Each device then
has its own function which allows to populate the device specific table.

"""
import numpy as np
import datetime
from struct import *
import mysql.connector
#import logging


# EMBEDDING Pylontech CLASS ----------------------------------------------------

class MySQL_com():
    """This class implements functions specific to the Pylontech US2000B Battery"""
    def __init__(self):
        ''' Constructor for this class. '''
        self._port = 0


    def __del__(self):
        ''' Destructor for this class. '''
        if self._port !=0:
            self.close()

    def open (self,HOST='localhost',USER ='grafanauser',PASSWORD='Mars2020',DATABASE='pumpdata',AUTH_PLUGIN='mysql_native_password'):
        """Establishing the connection to the mqsql database

        Args:
            HOST: network address of the server hosting the mysql database. Default='localhost'
            USER: mysql database user login for specified database. Default='grafanauser'
            PASSWORD: mysql database user password for specified user. Default='Mars2020'
            DATABASE: specifies the mysql database. Default='scpdata'
            AUTH_PLUGIN: specifies the login method to the mysql server. Default='mysql_native_password'

        Returns: Boolean value True or False

        """
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



    def write_PS(self, PS_LIST):
        """This function writes the parsed data into the mysql database table for the pump system monitor setup and returns a boolean value
        if the write process was sucessful.

        Args:
            PS_LIST: containing:
            [Water Level, System Temperature, Pump 1 Status, Pump 2 Status, Pump 3 Status, System Fault] dtype=float64 and dtype=str.


        DROP TABLE IF EXISTS `pump_data`;
        CREATE TABLE `pump_data` (
            `ts` datetime NOT NULL,
            `water_level` float DEFAULT (NULL),
            `temperature` float DEFAULT (NULL),
            `pump1_status` varchar(16) DEFAULT (NULL),
            `pump2_status` varchar(16) DEFAULT (NULL),
            `pump3_status` varchar(16) DEFAULT (NULL),
            `system_status` varchar(16) DEFAULT (NULL),
            PRIMARY KEY (`ts`),
            KEY `idx` (`ts`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;


        Returns: Boolean value True or False

        """


        tmp_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,datetime.datetime.now().hour,datetime.datetime.now().minute,datetime.datetime.now().second)
        cursor = self._port.cursor()
        tmp_PS = PS_LIST

        # Preparing SQL query to INSERT a record into the database.
        tmp_sql = "INSERT INTO pump_data (ts,water_level,temperature,pump1_status,pump2_status,pump3_status,system_status) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        tmp_val = [(tmp_time, tmp_PS[0][0], tmp_PS[0][1], tmp_PS[0][2], tmp_PS[0][3], tmp_PS[0][4], tmp_PS[0][5])]

        try:
            # Executing the SQL command
            cursor.executemany(tmp_sql, tmp_val)
            # print(cursor.rowcount, "records inserted.")
            # Commit your changes in the database
            self._port.commit()
            # print("successfully send data to database")
            return True
        except:
            # Rolling back in case of error
            self._port.rollback()
            print("Failed to send data to database")
            return False


