import asyncio
from utils.db import DB

db = DB()

class BotResponses:
    async def salutation(self) -> str:
        return """Bem vindo ao atendimento ByHI.
        Por favor, informe o CPF/CNPJ que seja atendimento."""

    async def request_name(self) -> str:
        return """Ainda não existe um cadastro para o documento informado, vamos fazer isso agora!
        Por favor, informe seu nome completo."""

    async def request_name_change(self) -> str:
        return """Certo, então vamo alterar seu cadastro!
        Por favor, informe seu nome completo."""

    async def confirm_name(self, name) -> str:
        return f"""Encontrei um cadastro com este documento.
        {name}
        Seu nome está correto?"""

    async def request_email(self) -> str:
        return """Por favor, me informe um email para contato.
        Lembrando que utilizaremos este email para te atualizar sobre qualquer novidade no futuro.
        É importante que seja um email válido."""

    async def invalid_document(self) -> str:
        return "Documento inválido. Por favor, informe um CPF/CNPJ válido."

    async def invalid_bool(self) -> str:
        return "Desculpe, não entendi. Tente responder 'Sim' ou 'Não'."