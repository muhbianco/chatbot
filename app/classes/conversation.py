import asyncio
from utils.db import DB

db = DB()

class Conversation:
    
    def __init__(self, contact_number):
        self.contact_number = contact_number

    async def is_exists(self) -> dict:
        q = "SELECT 1 FROM conversations WHERE phone_number=%s"
        return await db.fetchone(q, (self.contact_number, ))

    async def create_conversation(self):
        await db.insert("INSERT INTO conversations (`phone_number`, `step`) VALUES (%s, %s)", (self.contact_number, 1, ))

    async def forward_step(self, step):
        await db.update("UPDATE conversations SET step=%s WHERE phone_number=%s", (step, self.contact_number, ))

    async def step(self) -> float:
        r = await db.fetchone("SELECT step FROM conversations WHERE phone_number=%s", (self.contact_number, ))
        return float(r["step"])

    async def set_document(self, document):
        return await db.update("UPDATE conversations SET document=%s WHERE phone_number=%s", (document, self.contact_number, ))

    async def get_document(self) -> str:
        r = await db.fetchone("SELECT document FROM conversations WHERE phone_number=%s", (self.contact_number, ))
        return r["document"]

    async def close(self):
        await db.delete("DELETE FROM conversations WHERE phone_number=%s", (self.contact_number, ))

    async def get_robot_name(self) -> str:
        r = await db.fetchone("SELECT robot_code FROM conversations WHERE phone_number=%s", (self.contact_number, ))
        return r["robot_code"]