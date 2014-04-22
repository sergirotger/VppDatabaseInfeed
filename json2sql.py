"""
json2sql.py
This python scrip defines all the classes and function required for transforming the
JSON files received from the Ecosense RabbitMQ to SQL commands to introduce the data
into the VPP database.

Version 0.1
Date 22/04/2014
Developed by Sergi Rotger Griful <srgr@eng.au.dk>
"""

__author__ = 'srgr'
__version__ = '0.1'
__date__ = '21-04-2014'

import json
import unittest


class JsonString(object):
    """
    JsonString class defines the received string from the RabbitMQ server. It is composed by an identification text,
    composed by 8 characters, and a json file with the information.
    """

    def __init__(self, json_string='GFKXX00Y{"version":"??","timestamp":"2013-12-17T12:52:30Z", "others":[]}'):
        self.type = json_string[0:8]
        self.json = json.loads(json_string[8:])


class GFKRE003(JsonString):
    """
    Reading class defines the GFKRE003 JSON strings.
    """

    def sensor_mapping(self, dic):
        """
        Update the mapping sensor id sensor apartment in a dictionary.
        """
        for meas in self.json['reading']:
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
        for meas in self.json['reading']:
            aux = "( %s, %s, '%s')" % (meas['sensorId'], meas['value'], meas['timestamp'])
            sql_query += base + aux + ";\n"
        return sql_query


class GFKSC002(JsonString):
    """
    Reading class defines the GFKSC002 JSON strings.
    """

    def json2sql_apartments(self):
        """
        Returns a string with the SQL query to introduce the JSON file into the PostreSQL database.
        """
        base = "INSERT INTO Apartments (apartment_id, number, floor, size) VALUES"
        sql_query = ''
        for ap in self.json['appartmentCharacteristic']:
            aux = "( %s, %s, %s, %s)" % (ap['appartmentId'], ap['no'], ap['floor'], ap['size'])
            sql_query += base + aux + ";\n"
        return sql_query

    def json2sql_sensor(self, sensor_mapping):
        """
        Returns a string with the SQL query to introduce the JSON file into the PostreSQL database.
        """
        base = "INSERT INTO Sensor (sensor_id, description, unit, apartment_id) VALUES"
        sql_query = ''
        for sen in self.json['sensorCharacteristic']:
            aux = "( %s, '%s', '%s', %s)" % (
                sen['sensorId'], sen['description'], sen['unit'], sensor_mapping[sen['sensorId']])
            sql_query += base + aux + ";\n"
        return sql_query


class TestDefinedClasses(unittest.TestCase):
    """
    Defines the test for the defined classes.
    """
    def setUp(self):
        f = open('json_format_example.txt', 'r')
        self.reading = f.readline().replace('\n', '')
        self.characteristic = f.readline().replace('\n', '')
        f.close()

    def test_gfkre003(self):
        # Testing functionality of GFKRE003 class
        aux1 = GFKRE003(self.reading)
        self.assertEqual(aux1.type, 'GFKRE003')
        dic = {}
        aux1.sensor_mapping(dic)
        self.assertEqual(dic, {1: 1, 2: 2})
        print("GFKRE003 successfully tested")

    def test_gfksc002(self):
        # Testing functionality of GFKSC002 class
        aux2 = GFKSC002(self.characteristic)
        self.assertEqual(aux2.type, 'GFKSC002')
        self.assertEqual(aux2.json2sql_apartments(),
                         'INSERT INTO Apartments (apartment_id, number, floor, size) VALUES( 1, 7, 4, 16);\nINSERT' +
                         ' INTO Apartments (apartment_id, number, floor, size) VALUES( 2, 1, 3, 100);\n')
        aux1 = GFKRE003(self.reading)
        dic = {}
        aux1.sensor_mapping(dic)
        self.assertEqual(aux2.json2sql_sensor(dic),
                         "INSERT INTO Sensor (sensor_id, description, unit, apartment_id) VALUES" +
                         "( 1, 'CO2 Level', '%', 1);\nINSERT INTO Sensor (sensor_id, description, unit, apartment_id)" +
                         " VALUES( 2, 'CO2 Level', '%', 2);\n")

        print("GFKSC002 successfully tested")

if __name__ == '__main__':
            unittest.main()
