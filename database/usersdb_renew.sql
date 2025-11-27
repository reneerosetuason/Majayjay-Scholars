-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: usersdb
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `renew`
--

DROP TABLE IF EXISTS `renew`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `renew` (
  `renewal_id` int NOT NULL AUTO_INCREMENT,
  `application_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `student_id` varchar(100) DEFAULT NULL,
  `address` varchar(500) DEFAULT NULL,
  `course` varchar(255) DEFAULT NULL,
  `year_level` varchar(50) DEFAULT NULL,
  `gwa` decimal(3,2) DEFAULT NULL,
  `reason` text,
  `school_id` varchar(255) DEFAULT NULL,
  `id_picture` varchar(255) DEFAULT NULL,
  `birth_certificate` varchar(255) DEFAULT NULL,
  `grades` varchar(255) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `submission_date` timestamp NULL DEFAULT NULL,
  `scholarship_type` varchar(45) DEFAULT NULL,
  `contact_number` varchar(50) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `municipality` varchar(50) DEFAULT NULL,
  `baranggay` varchar(45) DEFAULT NULL,
  `cor` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`renewal_id`),
  CONSTRAINT `fk_renew_first_name` FOREIGN KEY (`first_name`) REFERENCES `application` (`first_name`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_renew_middle_name` FOREIGN KEY (`middle_name`) REFERENCES `application` (`middle_name`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_renew_last_name` FOREIGN KEY (`last_name`) REFERENCES `application` (`last_name`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_renew_address` FOREIGN KEY (`address`) REFERENCES `application` (`address`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_renew_municipality` FOREIGN KEY (`municipality`) REFERENCES `application` (`municipality`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_renew_baranggay` FOREIGN KEY (`baranggay`) REFERENCES `application` (`baranggay`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `renew`
--

LOCK TABLES `renew` WRITE;
/*!40000 ALTER TABLE `renew` DISABLE KEYS */;
INSERT INTO `renew` (`renewal_id`,`application_id`,`user_id`,`student_id`,`address`,`course`,`year_level`,`gwa`,`reason`,`school_id`,`id_picture`,`birth_certificate`,`grades`,`status`,`submission_date`,`scholarship_type`,`contact_number`,`first_name`,`middle_name`,`last_name`,`municipality`,`baranggay`,`cor`) VALUES (1,3,NULL,'0124-1192','Heahs street, brgy. asdhuw, ojashdh, ashc','BS Information Technology','2nd Year',1.07,'asdasd','6091200315605584916.jpg','6091200315605584916.jpg','6091200315605584916.jpg','6091200315605584916.jpg','Pending','2025-11-24 02:44:23','Mayor\'s Scholar','09120121201','Renee Rose','Dela Cruz','Tuason','Majayjay','Ibabang Bayucain','6091200315605584916.jpg'),(2,8,NULL,'0124-1192','Heahs street, brgy. asdhuw, ojashdh, ashc','BS Information Technology','2nd Year',1.07,'asdasd','6091200315605584916.jpg','6091200315605584916.jpg','6091200315605584916.jpg','6091200315605584916.jpg','Pending','2025-11-26 03:53:27',NULL,'09120121201','Renee Rose','Dela Cruz','Tuason','Majayjay','Burgos','6091200315605584916.jpg'),(3,8,NULL,'0124-1192','Heahs street, brgy. asdhuw, ojashdh, ashc','BS Information Technology','2nd Year',1.07,'asdasd','6091200315605584916.jpg','6091200315605584916.jpg','6091200315605584916.jpg','6091200315605584916.jpg','Pending','2025-11-26 04:01:24',NULL,'09120121201','Renee Rose','Dela Cruz','Tuason','Majayjay','Banti','6091200315605584916.jpg');
/*!40000 ALTER TABLE `renew` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-26 18:29:13
