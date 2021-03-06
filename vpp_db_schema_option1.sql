CREATE TABLE IF NOT EXISTS Apartments(
apartment_id INT NULL,
number INT NULL,
floor INT NULL,
size FLOAT NULL,
PRIMARY KEY(apartment_id)
);

CREATE TABLE IF NOT EXISTS Sensors(
sensor_id INT NULL,
description TEXT NULL,
unit TEXT NULL,
apartment_id INT NULL,
PRIMARY KEY(sensor_id),
FOREIGN KEY(apartment_id) REFERENCES apartments (apartment_id)
);

CREATE TABLE IF NOT EXISTS Measurements(
sensor_id INT NULL,
value FLOAT NULL,
datetime TIMESTAMP WITH TIME ZONE NULL,
PRIMARY KEY(sensor_id,datetime),
FOREIGN KEY (sensor_id)  REFERENCES sensors (sensor_id)
);


