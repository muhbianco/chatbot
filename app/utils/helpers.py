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
	afirmative = ["sim", "yes", "si", "s", "y"]
	negative = ["nao", "no", "not", "n"]
	message = unidecode(message_content.lower().replace(" ", ""))
	if message in afirmative:
		return True
	elif message in negative:
		return False
	else:
		return None

async def valid_phone_number(message_content) -> bool:
	if len(message_content) < 17:
		return False
	if "-" not in message_content:
		return False
	only_numbers = re.sub(r'[^0-9]', '', message_content)
	if len(only_numbers) < 13:
		return False
	return True

async def check_request_options(message_content) -> (bool, int):
	options = [1, 2]
	only_numbers = re.sub(r'[^0-9]', '', message_content)
	if int(only_numbers) not in options:
		return (False, only_numbers)
	return (True, only_numbers)