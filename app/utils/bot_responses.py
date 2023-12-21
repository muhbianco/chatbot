import asyncio
from utils.db import DB

db = DB()

class BotResponses:
    async def salutation(self) -> str:
        return """Bem vindo ao ROBÔ de atendimento automático do SAC BYHI! Estamos aqui para ajudar!
Por favor, informe o CPF/CNPJ que deseja atendimento. Informe somente os números do documento e aguarde a resposta do ROBÔ."""

    async def request_name(self) -> str:
        return """Ainda não existe um cadastro para o documento informado em nosso SAC, vamos fazer isso agora!
Por favor, informe seu nome completo e aguarde o ROBÔ responder."""

    async def request_name_change(self) -> str:
        return """Certo, então vamo alterar seu cadastro!
Por favor, informe seu somente nome completo e aguarde o ROBÔ responder."""

    async def request_email_change(self) -> str:
        return """Certo, então vamo alterar seu cadastro!
Por favor, informe seu novo e-mail somente e aguarde o ROBÔ responder."""

    async def confirm_name(self, name) -> str:
        return f"""Encontrei um cadastro com este documento.
{name}
Seu nome está correto? Digite SIM para confirmar ou NÃO para altera-lo."""

    async def confirm_email(self, email) -> str:
        return f"""{email}
Seu e-mail está correto? Digite SIM para confirmar ou NÃO para altera-lo."""

    async def request_email(self) -> str:
        return """Por favor, me informe um email para contato.
Lembrando que utilizaremos este email para te atualizar sobre qualquer novidade no futuro.
É importante que seja um email válido."""

    async def invalid_document(self) -> str:
        return "Documento inválido. Por favor, informe um CPF/CNPJ válido. Digite somente o CPF e aguarde o robô responder! Tente novamente."

    async def invalid_bool(self) -> str:
        return "Desculpe, não entendi. Tente responder SIM ou NÃO somente e aguarde o ROBÔ responder."

    async def invalid_option(self) -> str:
        return "Desculpe, opção inválida. Tente responder exatamente o que o robô pedir. Não utilize fotos e prints para responder, somente texto. Tente novamente."

    async def general_error(self) -> str:
        return "Desculpe, ocorreu um erro. Pode enviar a mensagem novamente?"

    async def confirm_request(self, ticket_number, ticket_request) -> str:
        if ticket_request == "produto":
            return f"""Certo, encontramos o protocolo {ticket_number} de atendimento já em tratativa.
Você deseja receber o produto, correto? Digite SIM para confirmar ou NÃO para alterar o atendimento desejado."""
        elif ticket_request == "estorno":
            return f"""Certo, encontramos o protocolo {ticket_number} de atendimento já em tratativa.
Você deseja receber o estorno do valor pago, correto? Digite SIM para confirmar ou NÃO para alterar o atendimento desejado."""
        else:
            return f"""Certo, encontramos o protocolo {ticket_number} de atendimento já em tratativa.
Seu problema é {ticket_request}, correto? Digite SIM para confirmar ou NÃO para alterar o atendimento desejado."""

    async def request_request(self, ticket_number = "") -> str:
        if ticket_number:
            return f"""Certo, anote seu protocolo de atendimento. {ticket_number}.
Digite 1 caso queira receber o produto.
Digite 2 caso queira receber o estorno da compra."""
        else:
            return """Digite 1 caso queira receber o produto.
Digite 2 caso queira receber o estorno da compra."""

    async def closure(self) -> str:
        return f"""Obrigado. Já coletamos todas as informações necessárias.
Enviaremos um e-mail com o protocolo.
Os próximos contatos de nosso SAC serão somente por e-mail. O contato via Whatsapp é 100% automatizado.
Peço por favor que aguarde. Nossa equipe entrará em contato o mais breve possível.
Fique atento a seu e-mail. Confirme em sua caixa de spam, caso necessário.
Atenciosamente, SAC BYHI."""

    async def invalid_email(self) -> str:
        return f"Por favor, informe um email válido. Digite somente o e-mail e aguarde o ROBÔ responder! Tente novamente."

    async def name_is_correct(self, client_name) -> str:
        return f"""{client_name}
Seu nome está correto? Digite SIM para confirmar ou NÃO para altera-lo."""

    async def request_pix_key(self) -> str:
        return "Por favor, nos informe a chave pix que deseja receber o reembolso. Digite em uma única mensagem."

    async def request_chart_list(self) -> str:
        return "Por favor, nos envie em uma única mensagem todos os produtos que comprou e aguarde o ROBÔ anotar seu pedido. Não utilize prints ou fotos. Somente texto."

    async def request_chart_confirm(self, chart_list) -> str:
        return f"""Certo, confira a lista de produtos do seu pedido:
{chart_list}
Está correto? Digite SIM para confirmar ou NÃO para altera-la."""

    async def request_seller(self) -> str:
        return f"""Você lembra por qual vendedor foi atendido?
Caso sim, digite o nome do vendedor. Caso não lembre, apenas digite NÃO e aguarde o ROBÔ responder."""

    async def request_seller_confirm(self, name_seller) -> str:
        return f"""{name_seller}
Este é o nome do vendedor? Digite SIM para confirmar ou NÃO para altera-lo."""

    async def request_pix_confirm(self, pix_key) -> str:
        return f"""{pix_key}
Sua chave pix está correta? Digite SIM para confirmar ou NÃO para altera-la."""