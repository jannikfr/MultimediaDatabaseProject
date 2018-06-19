# !/usr/bin/python
import json
from configparser import ConfigParser
import psycopg2


def connect():
    """
    Create a connection to the PostgreSQL database.
    :return: Connection object
    """

    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        print("Connected to database.")
        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def close_connection(conn):
    """
    Close database connection.
    :param conn: Connection object
    """
    conn.close()
    print("Disconnected from database.")


def config(filename='database.ini', section='postgresql'):
    """
    Read the .ini containing the database credentials and store them in a dictionary.
    :param filename: file name of the configuration .ini
    :param section: corresponding section of the .ini
    :return: Dictionary containing the database credentials
    """
    # Create a parser
    parser = ConfigParser()
    # Read config file
    parser.read(filename)

    # Get section
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def write_image_to_database(conn, image):
    """
    Inserts the image's features to the database.
    :param conn: connection object to access the database
    :param image: image object, whose features need to be stored in the database
    """

    sql = """INSERT INTO mmdbs_image(path, classification, local_histogram, global_histogram) VALUES(%s, %s) """

    try:
        # Create a new cursor
        cur = conn.cursor()
        # Execute the INSERT statement
        cur.execute(sql, (
        image.path, image.classification, json.dumps(image.local_histogram), json.dumps(image.global_histogram),))
        # Commit the changes to the database
        conn.commit()

        print("Saved image " + image.path + " to database.")

        # Close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_image(conn):
    sql = """SELECT path FROM mmdbs_image LIMIT 1"""

    try:
        # Create a new cursor
        cur = conn.cursor()
        # Execute the SELECT statement
        cur.execute(sql)
        # Close communication with the database
        cur.close()
        return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def get_count_images():
    sql = """SELECT count(id) FROM mmdbs_image"""

    try:

        conn = connect()

        # Create a new cursor
        cur = conn.cursor()

        # Execute the SELECT statement
        cur.execute(sql)

        theResult = cur.fetchone()
        print(theResult)
        return theResult
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)