import sys
import os

projeto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(projeto_dir)

from app.utils.db import DB

db = DB()

async def up():
	await db.query("ALTER TABLE tickets ADD COLUMN `chart` longtext after `request`")
	await db.query("ALTER TABLE tickets ADD COLUMN `seller` varchar(100) after `request`")

async def down():
	await db.query("ALTER TABLE tickets DROP COLUMN `chart`")
	await db.query("ALTER TABLE tickets DROP COLUMN `seller`")