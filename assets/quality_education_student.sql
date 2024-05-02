-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: quality_education
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `student_name` varchar(30) NOT NULL,
  `student_email` varchar(50) NOT NULL,
  `student_birthday` date DEFAULT NULL,
  `phone` varchar(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `picture` blob,
  `role` varchar(20) NOT NULL DEFAULT 'student',
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `student_id` (`student_id`),
  UNIQUE KEY `student_name` (`student_name`),
  UNIQUE KEY `student_email` (`student_email`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1,'Samuel Alvian','test@gmail.com','2024-04-30','087700595558','2024-04-25 05:04:23','2024-04-24 22:04:23',_binary '6‰\Þ','student','$2b$12$ywYCmFvLhWCSaHYXNuzLJ.mX0d5nYv5oJUEB/L1ZESWyQY.jwpEjK'),(3,'Sam','test123@gmail.com','2024-04-30','0123456789','2024-04-25 05:06:17','2024-04-24 22:06:17',_binary '6‰\Þ','student','$2b$12$iHs22u286rRBL5BJ5MvI2.Styleq4BtfEseLWb1JF2CRhi4slfnDG'),(5,'Test dua','123test@gmail.com','2024-04-30','0123456999','2024-04-25 05:15:19','2024-04-24 22:15:20',_binary '6‰\Þ','student','$2b$12$fdV2TBn8tGU/TLSoIqjRke0pZzmsSjEirx0yzlNGvFNupLrZh93Ry'),(6,'UPSY','111test@gmail.com','2024-04-30','1234567891011','2024-04-25 05:19:50','2024-04-25 05:17:04',_binary '6‰\Þ','student','$2b$12$RwE07TegXdvXuRV3aWsfMOWGhU2xIzzXSsdConKK3qDiB3Y8cuORa'),(8,'KEVIN','kevin123@gmail.com','2024-04-30','88888888888888','2024-04-25 13:41:14','2024-04-25 07:01:43',_binary '6‰\Þ','student','$2b$12$EisejclDHrNSQcyM2skZqucdAseUMQP5To1rsxYGeWk4JCP9/pSPm');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-01 16:54:45
