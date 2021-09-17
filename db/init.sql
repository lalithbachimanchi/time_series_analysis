CREATE DATABASE data_analysis;
use data_analysis;

CREATE TABLE `sensor` (
  `sensor_id` int NOT NULL AUTO_INCREMENT,
  `sensor_name` varchar(120) DEFAULT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sensor_id`)
);


CREATE TABLE `sensor_info` (
  `sensor_info_id` int NOT NULL AUTO_INCREMENT,
  `sensor_id` int NOT NULL,
  `value` float NOT NULL,
  `captured_time` datetime NOT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sensor_info_id`),
  KEY `ix_sensor_info_sensor_id` (`sensor_id`),
  CONSTRAINT `sensor_info_ibfk_1` FOREIGN KEY (`sensor_id`) REFERENCES `sensor` (`sensor_id`)
);

