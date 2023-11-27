import re
import asyncio
from unidecode import unidecode
from utils.db import DB


async def get_document_type(message_content) -> str:
	document = re.sub(r'[^0-9]', '', message_content)
	return "CPF" if len(document) == 11 else "CNPJ"

async def strip_document(message_content) -> str:
	return re.sub(r'[^0-9]', '', message_content)

async def check_yes(message_content) -> bool | None:
	afirmative = ["sim", "yes", "s", "y"]
	negative = ["nao", "no", "not", "n"]
	message = unidecode(message_content.lower())
	if message in afirmative:
		return True
	elif message in negative:
		return False
	else:
		return None
