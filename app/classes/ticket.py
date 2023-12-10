import asyncio
from datetime import datetime
from utils.db import DB

db = DB()

class Ticket:
    
    def __init__(self, client):
        self.document = client.document
        self.contact_number = client.contact_number

    async def get_client_ticket(self) -> str | None:
        r = await db.fetchone("SELECT ticket FROM tickets WHERE document=%s AND status IN('INPROCESS')", (self.document, ))
        return r["ticket"] if r else None

    async def get_request(self) -> str:
        r = await db.fetchone("SELECT request FROM tickets WHERE document=%s AND status IN('INPROCESS')", (self.document, ))
        return r["request"]

    async def create_client_ticket(self):
        now = datetime.now()
        ticket = now.strftime("%Y%m%d%H%M%S%f")[:-3]
        await db.insert("""
            INSERT INTO tickets (`document`, `ticket`, `status`)
            VALUES (%s, %s, %s)
        """, (self.document, ticket, "INPROCESS", ))

    async def set_client_request(self, option_number):
        request = "produto" if int(option_number) == 1 else "estorno"
        await db.update("UPDATE tickets SET request=%s WHERE document=%s", (request, self.document, ))

    async def set_chart(self, chart_list):
        await db.update("UPDATE tickets SET chart=%s WHERE document=%s", (chart_list, self.document, ))

    async def get_chart_list(self) -> str:
        r = await db.fetchone("SELECT chart FROM tickets WHERE document=%s AND status IN('INPROCESS')", (self.document, ))
        return r["chart"]

    async def set_seller(self, name_seller):
        await db.update("UPDATE tickets SET chart=%s WHERE document=%s", (name_seller, self.document, ))

    async def get_seller(self) -> str:
        r = await db.fetchone("SELECT seller FROM tickets WHERE document=%s AND status IN('INPROCESS')", (self.document, ))
        return r["seller"]

    async def set_pix_key(self, pix_key):
        await db.update("UPDATE tickets SET pix=%s WHERE document=%s", (pix_key, self.document, ))

    async def get_pix_key(self) -> str:
        r = await db.fetchone("SELECT pix FROM tickets WHERE document=%s AND status IN('INPROCESS')", (self.document, ))
        return r["pix"]