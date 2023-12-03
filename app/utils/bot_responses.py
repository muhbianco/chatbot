import asyncio
from utils.db import DB

db = DB()

class BotResponses:
    async def salutation(self) -> str:
        return """Bem vindo ao atendimento ByHI.
        Por favor, informe o CPF/CNPJ que deseja atendimento."""

    async def request_name(self) -> str:
        return """Ainda não existe um cadastro para o documento informado, vamos fazer isso agora!
        Por favor, informe seu nome completo."""

    async def request_name_change(self) -> str:
        return """Certo, então vamo alterar seu cadastro!
        Por favor, informe seu nome completo."""

    async def request_email_change(self) -> str:
        return """Certo, então vamo alterar seu cadastro!
        Por favor, informe seu novo e-mail."""

    async def confirm_name(self, name) -> str:
        return f"""Encontrei um cadastro com este documento.
        {name}
        Seu nome está correto?"""

    async def confirm_email(self, email) -> str:
        return f"""{email}
        Seu e-mail está correto?"""

    async def request_email(self) -> str:
        return """Por favor, me informe um email para contato.
        Lembrando que utilizaremos este email para te atualizar sobre qualquer novidade no futuro.
        É importante que seja um email válido."""

    async def invalid_document(self) -> str:
        return "Documento inválido. Por favor, informe um CPF/CNPJ válido."

    async def invalid_bool(self) -> str:
        return "Desculpe, não entendi. Tente responder 'Sim' ou 'Não'."

    async def invalid_option(self) -> str:
        return "Desculpe, opção inválida. Tente novamente."

    async def general_error(self) -> str:
        return "Desculpe, ocorreu um erro. Pode enviar a mensagem novamente?"

    async def confirm_request(self, ticket_number, ticket_request) -> str:
        if ticket_request == "produto":
            return f"""Certo, encontramos o protocolo {ticket_number} de atendimento já em tratativa.
            Você deseja receber o produto, correto?"""
        elif ticket_request == "estorno":
            return f"""Certo, encontramos o protocolo {ticket_number} de atendimento já em tratativa.
            Você deseja receber o estorno do valor pago, correto?"""
        else:
            return f"""Certo, encontramos o protocolo {ticket_number} de atendimento já em tratativa.
            Seu problema é {ticket_request}, correto?"""

    async def request_request(self, ticket_number) -> str:
        return f"""Certo, anote seu protocolo de atendimento. {ticket_number}.
        Digite:
        1 - Quero receber o produto.
        2 - Quero receber o estorno do pagamento."""

    async def closure(self) -> str:
        return f"""Obrigado. Já coletamos todas as informações necessárias.
        Peço por favor que aguarde. Nossa equipe entrará em contato o mais breve possível."""