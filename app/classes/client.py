import asyncio
from utils.db import DB
from utils.helpers import get_document_type

db = DB()

class Client:
    
    def __init__(self, document, contact_number):
        self.document = document
        self.contact_number = contact_number

    async def is_exists(self) -> dict:
        return await db.fetchone("SELECT 1 FROM clients WHERE document=%s", (self.document, ))

    async def create_client(self):
        document_type = await get_document_type(self.document)
        return await db.insert("""
            INSERT INTO clients (`phone_number`, `document`, `document_type`)
            VALUES (%s, %s, %s)
        """, (self.contact_number, self.document, document_type, ))

    async def set_name(self, name):
        return await db.update("UPDATE clients SET name=%s WHERE document=%s", (name, self.document, ))

    async def get_name(self) -> str:
        r = await db.fetchone("SELECT name FROM clients WHERE document=%s", (self.document, ))
        return r["name"]