-- MySQL dump 10.13  Distrib 8.0.38, for macos14 (arm64)
--
-- Host: 45.227.160.222    Database: uv029301_mstocks
-- ------------------------------------------------------
-- Server version	5.5.5-10.5.26-MariaDB-deb10

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
-- Table structure for table `mstocks_users`
--

DROP TABLE IF EXISTS `mstocks_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mstocks_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` char(32) NOT NULL,
  `name` varchar(300) NOT NULL,
  `email` varchar(255) NOT NULL,
  `role` int(1) NOT NULL,
  `date_added` date DEFAULT '0000-00-00',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mstocks_users`
--

LOCK TABLES `mstocks_users` WRITE;
/*!40000 ALTER TABLE `mstocks_users` DISABLE KEYS */;
INSERT INTO `mstocks_users` VALUES (1,'err','c5fa9f9c6492a3b96e597355f0636c0f','Enrique Richard','enrique.richard@gmail.com',1,'2017-04-01'),(2,'eugenio','9eff4f53802c2fb9de2fa0b86c84574b','Eugenio','egingratta@gmail.com',1,NULL),(4,'claudia','7bed69328582b9de3d9c868d058bbac2','Claudia','egingratta@gmail.com',1,NULL),(5,'heydi','c8cf8caf163b44e1cf4e66eb0ffbdf5b','Heydi','egingratta@gmail.com',4,NULL),(6,'ANGY','b7c1b9807afe03fd278931733705d01c','ANGELES','gaston.rodolfo@hotmail.com',4,NULL),(7,'santiago','7ad1655319b23ec421751edc3dc71801','santiago','singratta@gmail.com',4,NULL),(8,'singratta','16f67d3cde4c946985f4e5f94f1d2d4e','singratta','singratta@gmail.com',4,NULL),(9,'patricia','823fec7a2632ea7b498c1d0d11c11377','Patricia','eugenio@apasionadasxlamoda.com.ar',4,NULL),(10,'Helguera497','0f11efb410183ea7247b3e587d06bbca','Negocio','gaston.rodolfo@hotmail.com',4,NULL),(11,'camila','f5ffc847c2072ffb5fda82edd30bc19f','Camila','rrhh@apasionadasxlamoda.com.ar',4,NULL),(13,'Yesumi','184e1ca84620714f6986357e49ef9986','Yesumi','eingratta@beltex.com.ar',4,NULL),(14,'fernanda','789f0b383e4d871c1e1b3c376dd2a0b8','Fernanda','eingratta@beltex.com.ar',4,NULL);
/*!40000 ALTER TABLE `mstocks_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-20 11:22:57
