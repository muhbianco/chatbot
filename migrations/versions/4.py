import sys
import os

projeto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(projeto_dir)

from app.utils.db import DB

db = DB()

async def up():
	await db.query("ALTER TABLE conversations ADD COLUMN `robot_code` varchar(50)")

async def down():
	await db.query("ALTER TABLE conversations DROP COLUMN `robot_code`")