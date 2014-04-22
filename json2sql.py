"""
json2sql.py
This python scrip defines all the classes and function required for transforming the
JSON files received from the Ecosense RabbitMQ to SQL commands to introduce the data
into the VPP database.

Version 0.1
Date 21/04/2014
Developed by Sergi Rotger Griful <srgr@eng.au.dk>
"""

__author__ = 'srgr'
__version__ = '0.1'
__date__ = '21-04-2014'

import json


class JsonString(object):
    """
    JsonString class defines the received string from the RabbitMQ server. It is composed by an identification text,
    composed by 8 characters, and a json file with the information.
    data type of t
    """

    def __init__(self, json_string='GFKXX00Y{"version":"??","timestamp":"2013-12-17T12:52:30Z", "others":[]}'):
        self.type = json_string[0:7]
        self.json = json.loads(json_string[8:])


class GFKRE003(JsonString):
    """
    Reading class defines the functions with the
    """

    def sensor_mapping(self, dic={}):
        """
        Update the mapping sensor id sensor apartment in a dictionary
        """
        for meas in self.json['readings']:
            sen_id = meas['sensorId']
            ap_id = meas['appartmentId']
            dic[sen_id] = ap_id
        return dict

    def json2sql(self):
        """
        Returns a string with the SQL query to introduce the JSON file into the PostreSQL database.
        """
        base = "INSERT INTO Measurements (sensor_id, value, datetime) VALUES"
        sql_query = ''
        for meas in self.json['readings']:
            aux = "( %s, %s, '%s')" % (meas['sensorId'], meas['value'], meas['datetime'])
            sql_query += base + aux + ";\n"
        return sql_query


class GFKSC002(JsonString):
    """
    Reading class defines the functions with the
    """

    def json2sql_apartments(self):
        """
        Returns a string with the SQL query to introduce the JSON file into the PostreSQL database.
        """
        base = "INSERT INTO Apartments (apartment_id, number, floor, size) VALUES"
        sql_query = ''
        for ap in self.json['appartmentCharacteristic']:
            aux = "( %s, %s, %s, %s)" % (ap['apartmentId'], ap['no'], ap['floor'], ap['size'])
            sql_query += base + aux + ";\n"
        return sql_query

    def json2sql_sensor(self, sensor_mapping):
        """
        Returns a string with the SQL query to introduce the JSON file into the PostreSQL database.
        """
        base = "INSERT INTO Sensor (sensor_id, description, units, apartment_id) VALUES"
        sql_query = ''
        for sen in self.json['sensorCharacteristic']:
            aux = "( %s, '%s', '%s', %s)" % (
                sen['sensorId'], sen['description'], sen['units'], sensor_mapping[sen['sensorID']])
            sql_query += base + aux + ";\n"
        return sql_query


"""
The same with all the types
"""

sensor_id
INT
NOT
NULL,
description
TEXT
NULL,
units
TEXT
NULL,
apartment_id
INT
NULL,
