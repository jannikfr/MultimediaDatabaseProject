import json

import psycopg2


class DBConnection(object):

    def __init__(self):
        with open("config.json") as file_data:
            credentials = json.load(file_data)
        self.conn = psycopg2.connect(host=credentials['host'], user=credentials['user'],
                                     password=credentials['password'], database=credentials['db'],
                                     port=credentials['port'])

    def write_image_to_database(self, image):

        """ insert a new image into the mmdbs_image table """
        sql = """INSERT INTO mmdbs_image(path, classification) VALUES(%s, %s) """

        try:

            # create a new cursor
            cur = self.conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (image.path, image.classification,))
            # commit the changes to the database
            self.conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
