"""
filename: dbutils.py
Requires the driver:  conda install mysql-connector-python

description: A collection of database utilities to make it easier
to implement a database application
"""

import redis


class TwitterDBUtils:

    # %% Create a connection and clear the database
    def __init__(self, host, port, db, decode_responses):
        """ Future work: Implement connection pooling """
        self.con = redis.Redis(host=host,
                               port=port,
                               db=db,
                               decode_responses=decode_responses)


    def close(self):
        """ Close or release a connection back to the connection pool """
        self.con.close()
