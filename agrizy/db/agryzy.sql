-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.0.17-nt - MySQL Community Edition (GPL)
-- Server OS:                    Win32
-- HeidiSQL Version:             9.4.0.5174
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for agrizy
CREATE DATABASE IF NOT EXISTS `agrizy` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `agrizy`;

-- Dumping structure for table agrizy.admin
CREATE TABLE IF NOT EXISTS `admin` (
  `id` int(11) NOT NULL auto_increment,
  `email` varchar(50) NOT NULL default '0',
  `password` varchar(50) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table agrizy.admin: ~1 rows (approximately)
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` (`id`, `email`, `password`) VALUES
	(1, 'admin@gmail.com', '123');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;

-- Dumping structure for table agrizy.cart
CREATE TABLE IF NOT EXISTS `cart` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) default NULL,
  `product_id` int(11) default NULL,
  `quantity` int(11) default '1',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table agrizy.cart: ~0 rows (approximately)
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;

-- Dumping structure for table agrizy.consumers
CREATE TABLE IF NOT EXISTS `consumers` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) default NULL,
  `email` varchar(100) default NULL,
  `phone` varchar(15) default NULL,
  `state` varchar(50) default NULL,
  `city` varchar(50) default NULL,
  `pincode` varchar(10) default NULL,
  `password` varchar(255) default NULL,
  `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table agrizy.consumers: ~1 rows (approximately)
/*!40000 ALTER TABLE `consumers` DISABLE KEYS */;
INSERT INTO `consumers` (`id`, `name`, `email`, `phone`, `state`, `city`, `pincode`, `password`, `created_at`) VALUES
	(1, 'consumer', 'consumer@gmail.com', '9874563214', 'karnataka', 'mysore', '570004', '123', '2026-03-23 13:09:23');
/*!40000 ALTER TABLE `consumers` ENABLE KEYS */;

-- Dumping structure for table agrizy.farmers
CREATE TABLE IF NOT EXISTS `farmers` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) default NULL,
  `email` varchar(100) default NULL,
  `phone` varchar(15) default NULL,
  `aadhar` varchar(20) default NULL,
  `state` varchar(50) default NULL,
  `city` varchar(50) default NULL,
  `pincode` varchar(10) default NULL,
  `password` varchar(255) default NULL,
  `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `qr_image` varchar(255) default NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table agrizy.farmers: ~1 rows (approximately)
/*!40000 ALTER TABLE `farmers` DISABLE KEYS */;
INSERT INTO `farmers` (`id`, `name`, `email`, `phone`, `aadhar`, `state`, `city`, `pincode`, `password`, `created_at`, `qr_image`) VALUES
	(1, 'farmer', 'farmer@gmail.com', '9874563214', '741852741852', 'karnataka', 'mysore', '570004', '1234', '2026-03-23 12:36:00', 'PicsArt_10-01-11.33.46.jpg');
/*!40000 ALTER TABLE `farmers` ENABLE KEYS */;

-- Dumping structure for table agrizy.orders
CREATE TABLE IF NOT EXISTS `orders` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) default NULL,
  `product_id` int(11) default NULL,
  `quantity` int(11) default NULL,
  `total_price` float default NULL,
  `order_date` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table agrizy.orders: ~0 rows (approximately)
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` (`id`, `user_id`, `product_id`, `quantity`, `total_price`, `order_date`) VALUES
	(1, 1, 1, 1, 5000, '2026-03-26 16:10:46');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;

-- Dumping structure for table agrizy.products
CREATE TABLE IF NOT EXISTS `products` (
  `id` int(11) NOT NULL auto_increment,
  `farmer_id` int(11) default NULL,
  `name` varchar(100) default NULL,
  `weight` varchar(50) default NULL,
  `price` decimal(10,2) default NULL,
  `description` text,
  `image` varchar(255) default NULL,
  `status` varchar(20) default 'pending',
  `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `availability` varchar(20) default 'available',
  `category` varchar(50) default 'Other',
  PRIMARY KEY  (`id`),
  KEY `farmer_id` (`farmer_id`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`farmer_id`) REFERENCES `farmers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table agrizy.products: ~2 rows (approximately)
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` (`id`, `farmer_id`, `name`, `weight`, `price`, `description`, `image`, `status`, `created_at`, `availability`) VALUES
	(1, 1, 'coffee', '10kg', 5000.00, 'haiguwg', 'logestic.png', 'approved', '2026-03-26 15:50:27', 'sold'),
	(2, 1, 'wheat', '50kg', 10000.00, 'asga', 'pocketemp.png', 'approved', '2026-03-26 15:50:43', 'sold');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;

-- Dumping structure for table agrizy.recart
CREATE TABLE IF NOT EXISTS `recart` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) default NULL,
  `product_id` int(11) default NULL,
  `quantity` int(11) default '1',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table agrizy.recart: ~0 rows (approximately)
/*!40000 ALTER TABLE `recart` DISABLE KEYS */;
/*!40000 ALTER TABLE `recart` ENABLE KEYS */;

-- Dumping structure for table agrizy.reorders
CREATE TABLE IF NOT EXISTS `reorders` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) default NULL,
  `product_id` int(11) default NULL,
  `quantity` int(11) default NULL,
  `total_price` float default NULL,
  `order_date` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table agrizy.reorders: ~0 rows (approximately)
/*!40000 ALTER TABLE `reorders` DISABLE KEYS */;
INSERT INTO `reorders` (`id`, `user_id`, `product_id`, `quantity`, `total_price`, `order_date`) VALUES
	(1, 1, 2, 1, 10000, '2026-03-26 16:14:04');
/*!40000 ALTER TABLE `reorders` ENABLE KEYS */;

-- Dumping structure for table agrizy.retailers
CREATE TABLE IF NOT EXISTS `retailers` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) default NULL,
  `email` varchar(100) default NULL,
  `phone` varchar(15) default NULL,
  `shop_name` varchar(100) default NULL,
  `state` varchar(50) default NULL,
  `city` varchar(50) default NULL,
  `pincode` varchar(10) default NULL,
  `password` varchar(255) default NULL,
  `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table agrizy.retailers: ~1 rows (approximately)
/*!40000 ALTER TABLE `retailers` DISABLE KEYS */;
INSERT INTO `retailers` (`id`, `name`, `email`, `phone`, `shop_name`, `state`, `city`, `pincode`, `password`, `created_at`) VALUES
	(1, 'retialer', 'retailer@gmail.com', '9874563214', 'abc', 'karnataka', 'mysore', '570004', '123', '2026-03-26 13:15:01');
/*!40000 ALTER TABLE `retailers` ENABLE KEYS */;

-- Dumping structure for table agrizy.retransactions
CREATE TABLE IF NOT EXISTS `retransactions` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) default NULL,
  `farmer_id` int(11) default NULL,
  `product_id` int(11) default NULL,
  `quantity` int(11) default NULL,
  `total_price` decimal(10,2) default NULL,
  `status` varchar(20) default 'paid',
  `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table agrizy.retransactions: ~0 rows (approximately)
/*!40000 ALTER TABLE `retransactions` DISABLE KEYS */;
INSERT INTO `retransactions` (`id`, `user_id`, `farmer_id`, `product_id`, `quantity`, `total_price`, `status`, `created_at`) VALUES
	(1, 1, 1, 2, 1, 10000.00, 'paid', '2026-03-26 16:14:04');
/*!40000 ALTER TABLE `retransactions` ENABLE KEYS */;

-- Dumping structure for table agrizy.transactions
CREATE TABLE IF NOT EXISTS `transactions` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) default NULL,
  `farmer_id` int(11) default NULL,
  `product_id` int(11) default NULL,
  `quantity` int(11) default NULL,
  `total_price` decimal(10,2) default NULL,
  `status` varchar(20) default 'paid',
  `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table agrizy.transactions: ~0 rows (approximately)
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` (`id`, `user_id`, `farmer_id`, `product_id`, `quantity`, `total_price`, `status`, `created_at`) VALUES
	(1, 1, 1, 1, 1, 5000.00, 'paid', '2026-03-26 16:10:46');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;

-- ========== FARMER COMMUNITY TABLES ==========

-- Groups that farmers can create and join
CREATE TABLE IF NOT EXISTS `community_groups` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(150) NOT NULL,
  `description` text,
  `category` varchar(50) DEFAULT 'General',
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `community_groups_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `farmers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Group membership
CREATE TABLE IF NOT EXISTS `group_members` (
  `id` int(11) NOT NULL auto_increment,
  `group_id` int(11) NOT NULL,
  `farmer_id` int(11) NOT NULL,
  `joined_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_membership` (`group_id`, `farmer_id`),
  KEY `group_id` (`group_id`),
  KEY `farmer_id` (`farmer_id`),
  CONSTRAINT `group_members_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `community_groups` (`id`),
  CONSTRAINT `group_members_ibfk_2` FOREIGN KEY (`farmer_id`) REFERENCES `farmers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Posts in the community feed or within a group
CREATE TABLE IF NOT EXISTS `community_posts` (
  `id` int(11) NOT NULL auto_increment,
  `farmer_id` int(11) NOT NULL,
  `group_id` int(11) DEFAULT NULL,
  `content` text NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `farmer_id` (`farmer_id`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `community_posts_ibfk_1` FOREIGN KEY (`farmer_id`) REFERENCES `farmers` (`id`),
  CONSTRAINT `community_posts_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `community_groups` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Comments on posts
CREATE TABLE IF NOT EXISTS `post_comments` (
  `id` int(11) NOT NULL auto_increment,
  `post_id` int(11) NOT NULL,
  `farmer_id` int(11) NOT NULL,
  `content` text NOT NULL,
  `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `post_id` (`post_id`),
  KEY `farmer_id` (`farmer_id`),
  CONSTRAINT `post_comments_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `community_posts` (`id`),
  CONSTRAINT `post_comments_ibfk_2` FOREIGN KEY (`farmer_id`) REFERENCES `farmers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Likes on posts
CREATE TABLE IF NOT EXISTS `post_likes` (
  `id` int(11) NOT NULL auto_increment,
  `post_id` int(11) NOT NULL,
  `farmer_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_like` (`post_id`, `farmer_id`),
  KEY `post_id` (`post_id`),
  KEY `farmer_id` (`farmer_id`),
  CONSTRAINT `post_likes_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `community_posts` (`id`),
  CONSTRAINT `post_likes_ibfk_2` FOREIGN KEY (`farmer_id`) REFERENCES `farmers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;