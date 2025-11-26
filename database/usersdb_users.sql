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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `password` varchar(225) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `user_type` varchar(45) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `bday` date DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `idx_user_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'ren@gmail.com','asdf','REN','mayor',NULL,NULL,NULL,NULL,NULL),(2,'ryzamae@gmail.com','asdf','Ryza','student',NULL,NULL,NULL,NULL,NULL),(3,'reneerosetuason@gmail.com','asdf',NULL,'student',NULL,NULL,NULL,NULL,NULL),(4,'rachelricaalmonte@gmail.com','asdf',NULL,'student',NULL,NULL,NULL,NULL,NULL),(5,'admin@scholar.com','asdf','admin','student',NULL,NULL,NULL,NULL,NULL),(6,'asdasdsad@gmail.com','asdasd','asdasdsad','student',NULL,NULL,NULL,NULL,NULL),(7,'admin@gmail.com','asdf','ren','admin',NULL,NULL,NULL,NULL,NULL),(8,'jaredtaih@gmail.com','asdf','jaredtaih','student',NULL,NULL,NULL,NULL,NULL),(9,'asdf@gmail.com','asdf','Renee Rose Dela Cruz Tuason','admin',NULL,NULL,NULL,NULL,NULL),(10,'qwer@gmail.com','asdf','Renee Rose Dela Cruz Tuason','mayor',NULL,NULL,NULL,NULL,NULL),(11,'romulojules16@gmail.com','asdf',NULL,'student','Jules Andrei','Romulo','Mejino',NULL,NULL),(12,'jsobrevinas6@gmail.com','asdf',NULL,'student','Justin','Sobrevinas','S',NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-26 18:29:12
