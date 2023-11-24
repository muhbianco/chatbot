import sys
import os

projeto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(projeto_dir)

from app.utils.db import DB

db = DB()

async def up():
	await db.query("""
		CREATE TABLE IF NOT EXISTS `schema_info` (`version` int(11) NOT NULL);
		INSERT INTO `schema_info` (version) VALUES (%s);
	""", (1, ))

	await db.query("""
		CREATE TABLE IF NOT EXISTS `clients` (
			`id` int(11) NOT NULL AUTO_INCREMENT,
			`create_date` timestamp DEFAULT current_timestamp(),
			`update_date` timestamp DEFAULT NULL ON UPDATE current_timestamp(),
			`name` varchar(100) NOT NULL,
			`phone_number` varchar(50) NOT NULL,
			`email` varchar(100) DEFAULT NULL,
			`document` varchar(14) DEFAULT NULL,
			`document_type` enum('CPF','CNPJ') DEFAULT NULL,
			PRIMARY KEY (`id`),
			UNIQUE KEY `phone_number` (`phone_number`),
			UNIQUE KEY `cpf` (`document`)
		)
	""")

	await db.query("""
		CREATE TABLE IF NOT EXISTS `tickets` (
			`id` int(11) NOT NULL AUTO_INCREMENT,
			`create_date` timestamp DEFAULT current_timestamp(),
			`update_date` timestamp DEFAULT NULL ON UPDATE current_timestamp(),
			`document` varchar(14) NOT NULL,
			`ticket` int(11) NOT NULL,
			`status` enum('INPROCESS', 'RESOLVED') DEFAULT NULL,
			`date_sale` timestamp DEFAULT NULL,
			`seller_name` varchar(100) DEFAULT NULL,
			`value` decimal(10, 2) DEFAULT NULL,
			PRIMARY KEY (`id`)
		)
	""")

	await db.query("""
		CREATE TABLE IF NOT EXISTS `conversations` (
			`id` int(11) NOT NULL AUTO_INCREMENT,
			`create_date` timestamp DEFAULT current_timestamp(),
			`close_date` timestamp DEFAULT NULL,
			`phone_number` varchar(50) NOT NULL,
			`step` int(11) NOT NULL,
			PRIMARY KEY (`id`),
			UNIQUE KEY `phone_number` (`phone_number`)
		)
	""")

async def down():
	await db.query("DROP TABLE IF EXISTS `schema_info`")
	await db.query("DROP TABLE IF EXISTS `clients`")
	await db.query("DROP TABLE IF EXISTS `tickets`")
	await db.query("DROP TABLE IF EXISTS `conversations`")