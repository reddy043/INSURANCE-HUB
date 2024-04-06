-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: insurance_operations
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (2,'Life Insurance 1','Provides coverage for a specified period of time or for the entire life of the insurence'),(3,'accidental insurance','Accident insurance is a type of insurance where the policy holder is paid directly in the event of an accident resulting in injury of the insured. ');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customerapplications`
--

DROP TABLE IF EXISTS `customerapplications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customerapplications` (
  `application_id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(255) DEFAULT NULL,
  `policy_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  `application_date` date DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `address` text,
  `average_income` decimal(10,2) DEFAULT NULL,
  `health` enum('Excellent','Good','Fair','Poor') DEFAULT NULL,
  `health_problems` text,
  `email` varchar(255) DEFAULT NULL,
  `policy_name` varchar(255) DEFAULT NULL,
  `category_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`application_id`),
  UNIQUE KEY `unique_email` (`email`),
  KEY `policy_id` (`policy_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `customerapplications_ibfk_2` FOREIGN KEY (`policy_id`) REFERENCES `policies` (`policy_id`),
  CONSTRAINT `customerapplications_ibfk_3` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customerapplications`
--

LOCK TABLES `customerapplications` WRITE;
/*!40000 ALTER TABLE `customerapplications` DISABLE KEYS */;
INSERT INTO `customerapplications` VALUES (10,'nagalakshmi',3,2,'2024-03-02','357689654','hdcg',97635.00,'Good','erewqqqwweq','nagalakshmi@codegnan.com','life','Life Insurance 1'),(12,'kesava',3,2,'2024-03-30','746832846','vijaywada',74832.00,'Good','no problems','kesava@codegnan.com','life','Life Insurance 1'),(16,'vijayalakshmi',4,3,'2024-03-30','783463724','vijayawada',78643.00,'Good','no problems','vijayalakshmi@codegnan.com','accidental','accidental insurance');
/*!40000 ALTER TABLE `customerapplications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customerregistrations`
--

DROP TABLE IF EXISTS `customerregistrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customerregistrations` (
  `cid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(70) DEFAULT NULL,
  `email` varchar(80) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `address` text,
  `password` varchar(30) DEFAULT NULL,
  `reply` text,
  `reply_date` date DEFAULT NULL,
  PRIMARY KEY (`cid`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customerregistrations`
--

LOCK TABLES `customerregistrations` WRITE;
/*!40000 ALTER TABLE `customerregistrations` DISABLE KEYS */;
INSERT INTO `customerregistrations` VALUES (1,'nnn','nagalakshmi@codegnan.com','43578943567','vij','nagu@123',NULL,NULL);
/*!40000 ALTER TABLE `customerregistrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inquiries`
--

DROP TABLE IF EXISTS `inquiries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inquiries` (
  `inquiry_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int DEFAULT NULL,
  `message` text,
  `inquiry_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `reply` text,
  PRIMARY KEY (`inquiry_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `inquiries_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customerregistrations` (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inquiries`
--

LOCK TABLES `inquiries` WRITE;
/*!40000 ALTER TABLE `inquiries` DISABLE KEYS */;
INSERT INTO `inquiries` VALUES (3,1,'how can i get the official documentation of insurance','2024-03-30 10:26:27',NULL);
/*!40000 ALTER TABLE `inquiries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `policies`
--

DROP TABLE IF EXISTS `policies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `policies` (
  `policy_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` text,
  `coverage_area` varchar(255) DEFAULT NULL,
  `premium` decimal(10,2) DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`policy_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `policies_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `policies`
--

LOCK TABLES `policies` WRITE;
/*!40000 ALTER TABLE `policies` DISABLE KEYS */;
INSERT INTO `policies` VALUES (3,'Life Insurance 1','Provides coverage for a specified period of time or for the entire life of the insured','life',500.00,2),(4,'accidental insurance','Accident insurance is a type of insurance where the policy holder is paid directly in the event of an accident resulting in injury of the insured. ','accidental',150.00,3);
/*!40000 ALTER TABLE `policies` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-30 16:12:14
