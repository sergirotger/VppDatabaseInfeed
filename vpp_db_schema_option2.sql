CREATE TABLE IF NOT EXISTS Measurements(
sensor_id INT NOT NULL,
value FLOAT NULL,
datetime TIMESTAMP WITH TIME ZONE NULL,
PRIMARY KEY(sensor_id,datetime),
);

CREATE TABLE IF NOT EXISTS Apartments(
apartment_id INT NOT NULL,
number INT NULL,
floor INT NULL,
size FLOAT NULL,
datetime TIMESTAMP WITH TIME ZONE NOT NULL,
PRIMARY KEY(apartment_id, datetime)
);

CREATE TABLE IF NOT EXISTS Sensors(
sensor_id INT NOT NULL,
description TEXT NULL,
units TEXT NULL,
datetime TIMESTAMP WITH TIME ZONE NOT NULL,
PRIMARY KEY(sensor_id, datetime)
);

CREATE TABLE IF NOT EXISTS SensorLocation (
sensor_id INT NOT NULL,
apartment_id INT NOT NULL,
datetime TIMESTAMP WITH TIME ZONE NOT NULL,
PRIMARY KEY (sensor_id, apartment_id, datetime)
);