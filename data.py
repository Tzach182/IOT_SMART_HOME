import sqlite3
from datetime import datetime
from mqtt_init import *
from sqlite3 import Error


def get_current_time():
    current_time = datetime.now()
    return str(current_time)


def create_connection(db_file=db_name):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        pp = ('Connected to version: ' + sqlite3.version)
        print(pp)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def init_db(database):
    table = """ CREATE TABLE IF NOT EXISTS `health` (
    `bodyTemperature` REAL NOT NULL,
	`pulseRate`	REAL NOT NULL,
	`respirationRate` REAL NOT NULL,
	`bloodPressure` REAL NOT NULL,
	`timestamp`	TEXT NOT NULL);"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create tables
        create_table(conn, table)
        conn.close()
    else:
        print("Error! cannot create the database connection.")


def insert_health_check(database, health_data):
    conn = create_connection(database)
    cursor = conn.cursor()

    with conn:
        cursor.execute("INSERT INTO health VALUES (:bodyTemperature ,:pulseRate, :respirationRate, :bloodPressure, :timestamp)",
                {
                    'bodyTemperature': float(health_data["bodyTemperature"]),
                    'pulseRate': float(health_data["pulseRate"]),
                    'respirationRate': float(health_data["respirationRate"]),
                    'bloodPressure': float(health_data["bloodPressure"]),
                    'timestamp': get_current_time()
                 })


def get_health_update(database):
    conn = create_connection(database)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM health")
    return cursor.fetchmany(10)



