-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: localhost    Database: grafanadata
-- ------------------------------------------------------
-- Server version	8.0.46-0ubuntu0.22.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `hcro_d300gc_generator`
--

DROP TABLE IF EXISTS `hcro_d300gc_generator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hcro_d300gc_generator` (
  `ts` datetime(3) NOT NULL,
  `generator` varchar(16) NOT NULL,
  `communication_status` varchar(16) DEFAULT NULL,
  `overall_status` varchar(16) DEFAULT NULL,
  `control_mode_code` smallint unsigned DEFAULT NULL,
  `control_mode` varchar(64) DEFAULT NULL,
  `auto_start_enabled` boolean DEFAULT NULL,
  `engine_state_code` smallint unsigned DEFAULT NULL,
  `engine_state` varchar(32) DEFAULT NULL,
  `oil_pressure_kpa` smallint unsigned DEFAULT NULL,
  `coolant_temperature_c` smallint DEFAULT NULL,
  `oil_temperature_c` smallint DEFAULT NULL,
  `fuel_level_pct` smallint unsigned DEFAULT NULL,
  `charge_alternator_voltage_v` decimal(4,1) DEFAULT NULL,
  `battery_voltage_v` decimal(4,1) DEFAULT NULL,
  `engine_speed_rpm` smallint unsigned DEFAULT NULL,
  `generator_frequency_hz` decimal(4,1) DEFAULT NULL,
  `generator_l1_n_voltage_v` decimal(8,1) DEFAULT NULL,
  `generator_l2_n_voltage_v` decimal(8,1) DEFAULT NULL,
  `generator_l3_n_voltage_v` decimal(8,1) DEFAULT NULL,
  `generator_l1_current_a` decimal(7,1) DEFAULT NULL,
  `generator_l2_current_a` decimal(7,1) DEFAULT NULL,
  `generator_l3_current_a` decimal(7,1) DEFAULT NULL,
  `generator_total_power_w` int DEFAULT NULL,
  `generator_power_factor` decimal(4,2) DEFAULT NULL,
  `engine_run_time_s` int unsigned DEFAULT NULL,
  `number_of_starts` int unsigned DEFAULT NULL,
  `generator_positive_kwh` decimal(11,1) DEFAULT NULL,
  `active_alarm_count` smallint unsigned DEFAULT NULL,
  `active_alarms` json DEFAULT NULL,
  PRIMARY KEY (`ts`,`generator`),
  KEY `idx_generator_ts` (`generator`,`ts`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-13 18:10:41
