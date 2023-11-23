import sys
import os

projeto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(projeto_dir)

from app.utils.db import DB

db = DB()

async def up():
	await db.query("""
		CREATE TABLE `clients` (
			`id` int(11) NOT NULL AUTO_INCREMENT,
			`create_date` timestamp NULL DEFAULT current_timestamp(),
			`update_date` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
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
		CREATE TABLE `conversations` (
			`id` int(11) NOT NULL AUTO_INCREMENT,
			`create_date` timestamp NULL DEFAULT current_timestamp(),
			`update_date` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
			`phone_number` varchar(50) NOT NULL,
			`step` int(11) NOT NULL DEFAULT 0,
			PRIMARY KEY (`id`),
			UNIQUE KEY `phone_number` (`phone_number`)
		)
	""")

async def down():
	await db.query("DROP TABLE `clients`")

	await db.query("DROP TABLE `conversations`")