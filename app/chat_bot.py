import asyncio
import re
import pprint
import traceback
import sys
from dotenv import load_dotenv
from pprint import pformat
from playwright.async_api import async_playwright
from pycpfcnpj import cpfcnpj
from email_validator import validate_email, EmailNotValidError

from utils.db import DB
from utils.helpers import *
from utils.bot_responses import BotResponses
from utils.mail import SendEmail

from classes.conversation import Conversation
from classes.client import Client
from classes.ticket import Ticket

db = DB()
responses = BotResponses()
mail = SendEmail()


async def check_unread_messages(page):
    # Pegue todas as conversas não lidas
    unread_chats = await page.query_selector_all('.aumms1qt')

    if unread_chats:
        # Se houver mensagens não lidas, clique na primeira
        await unread_chats[0].click()

        # Aguarde um momento para a mensagem ser carregada
        # await page.wait_for_timeout(2000)

        # Abre o contact info
        print("Esperando 01")
        await page.screenshot(path="test.png")
        await page.wait_for_selector(".AmmtE .kiiy14zj", timeout=0)
        await page.locator(".AmmtE .kiiy14zj").click()

        print("Esperando 02")
        await page.screenshot(path="test.png")
        await page.wait_for_selector(".iWqod._1MZM5._2BNs3", timeout=0)
        menu_buttons = await page.query_selector_all(".iWqod._1MZM5._2BNs3")
        await menu_buttons[0].click()

        # Coleta o numero de telefone do cliente
        contact_number = ""
        while not contact_number:
            # Abre o contact info
            print("Esperando 01")
            await page.screenshot(path="test.png")
            await page.wait_for_selector(".AmmtE .kiiy14zj", timeout=0)
            await page.locator(".AmmtE .kiiy14zj").click()

            print("Esperando 02")
            await page.screenshot(path="test.png")
            await page.wait_for_selector(".iWqod._1MZM5._2BNs3", timeout=0)
            menu_buttons = await page.query_selector_all(".iWqod._1MZM5._2BNs3")
            await menu_buttons[0].click()
            try:
                print("Esperando 03")
                await page.screenshot(path="test.png")
                await page.wait_for_selector(".q9lllk4z.e1gr2w1z.qfejxiq4", timeout=1000)
                contact_number = await page.locator(".q9lllk4z.e1gr2w1z.qfejxiq4").inner_text()
                if not await valid_phone_number(contact_number):
                    print("Esperando 04")
                    await page.screenshot(path="test.png")
                    await page.wait_for_selector(".enbbiyaj.e1gr2w1z.hp667wtd", timeout=1000)
                    contact_number = await page.locator(".enbbiyaj.e1gr2w1z.hp667wtd").inner_text()
            except Exception:
                await page.wait_for_selector(".kk3akd72.svlsagor.fewfhwl7.ajgl1lbb.ltyqj8pj", timeout=0)
                await page.locator(".kk3akd72.svlsagor.fewfhwl7.ajgl1lbb.ltyqj8pj").click()
                contact_number = ""

        print("Esperando 05")
        await page.screenshot(path="test.png")
        await page.wait_for_selector(".kk3akd72.svlsagor.fewfhwl7.ajgl1lbb.ltyqj8pj", timeout=0)
        await page.locator(".kk3akd72.svlsagor.fewfhwl7.ajgl1lbb.ltyqj8pj").click()
        await asyncio.sleep(2)

        # Pega a ultima mensagem enviada pelo cliente
        messages = await page.query_selector_all(".message-in ._1BOF7._2AOIt ._21Ahp ._11JPr.selectable-text.copyable-text")
        last_message_content = await messages[len(messages)-1].text_content()

        response = ""
        if not last_message_content:
            response = await responses.general_error()

        while not response:
            response = await message_treatment(page, contact_number, last_message_content)
            await asyncio.sleep(1)

        print("RESPOSTA PRONTA:::::", response)
        await page.screenshot(path="response.png")

        print("Esperando 06")
        await page.screenshot(path="test.png")
        await page.wait_for_selector("._3Uu1_ .to2l77zo.gfz4du6o.ag5g9lrv.bze30y65.kao4egtt", timeout=0)
        place_holder = await page.query_selector("._3Uu1_ .to2l77zo.gfz4du6o.ag5g9lrv.bze30y65.kao4egtt")
        await place_holder.focus()
        await place_holder.type(response)
        print("Esperando 07")
        await page.screenshot(path="response1.png")
        await page.wait_for_selector(".tvf2evcx.oq44ahr5.lb5m6g5c.svlsagor.p2rjqpw5.epia9gcq", timeout=0)
        await page.locator(".tvf2evcx.oq44ahr5.lb5m6g5c.svlsagor.p2rjqpw5.epia9gcq").click()
        await page.keyboard.press('Escape')

    else:
        print('Não há mensagens não lidas.')

async def message_treatment(page, contact_number, message_content) -> str:
    print("contact_number:::::::", contact_number)
    print("message_content:::::::", message_content)

    conversation = Conversation(contact_number)

    # Checa se já existe uma conversa ativa
    # Envia saudação e solicita o documento CNPJ/CPF
    if not await conversation.is_exists():
        await conversation.create_conversation()
        return await responses.salutation()
    elif document := await conversation.get_document():
        client = Client(document, contact_number)
        ticket = Ticket(client)

    conversation_step = await conversation.step()

    # Step 1 = Consulta o CPF da table clients
    # Cria o contato e solicita o Nome completo
    if conversation_step == 1:
        document = await strip_document(message_content)
        client = Client(document, contact_number)
        await conversation.set_document(document)

        if cpfcnpj.validate(document):
            if not await client.is_exists():
                client_id = await client.create_client()
                await conversation.forward_step(1.2)
                return await responses.request_name()
            else:
                client_name = await client.get_name()
                if client_name:
                    await conversation.forward_step(1.1)
                    return await responses.confirm_name(client_name)
                else:
                    await conversation.forward_step(1.2)
                    return await responses.request_name()
        else:
            return await responses.invalid_document()

    # Step 1.1 = Trata a resposta confirmação do nome existente
    elif conversation_step == 1.1:
        r = await check_yes(message_content)
        if r is None:
            return await responses.invalid_bool()
        elif r is False:
            await conversation.forward_step(1.2)
            return await responses.request_name_change()
        elif r is True:
            client_email = await client.get_email()
            if client_email:
                await conversation.forward_step(2.1)
                return await responses.confirm_email(client_email)
            else:
                await conversation.forward_step(3)
                return await responses.request_email()

    # Step 1.2 = Confirme nome
    elif conversation_step == 1.2:
        await conversation.forward_step(1.1)
        await client.set_name(message_content)
        return await responses.name_is_correct(message_content)

    # Step 2 = Salva o nome informado e solicita o email
    elif conversation_step == 2:
        await client.set_name(message_content)
        client_email = await client.get_email()
        if client_email:
            await conversation.forward_step(2.1)
            return await responses.confirm_email(client_email)
        else:
            await conversation.forward_step(3)
            return await responses.request_email()

    # Step 2.1 = Trata a resposta confirmação do email existente
    elif conversation_step == 2.1:
        r = await check_yes(message_content)
        if r is None:
            return await responses.invalid_bool()
        elif r is False:
            await conversation.forward_step(3)
            return await responses.request_email_change()
        elif r is True:
            if ticket_number := await ticket.get_client_ticket():
                ticket_request = await ticket.get_request()
                if ticket_request is not None:
                    await conversation.forward_step(3.1)
                    return await responses.confirm_request(ticket_number, ticket_request)
                else:
                    await conversation.forward_step(4)
                    return await responses.request_request(ticket_number)
            else:
                await ticket.create_client_ticket()
                ticket_number = await ticket.get_client_ticket()
                await conversation.forward_step(4)
                return await responses.request_request(ticket_number)

    # Step 3 = Recebe o email
    elif conversation_step == 3:
        try:
            email_info = validate_email(message_content, check_deliverability=False)
            client_email = email_info.normalized
        except EmailNotValidError as e:
            return await responses.invalid_email()
        await client.set_email(client_email)
        if ticket_number := await ticket.get_client_ticket():
            ticket_request = await ticket.get_request()
            if ticket_request is not None:
                await conversation.forward_step(3.1)
                return await responses.confirm_request(ticket_number, ticket_request)
            else:
                await conversation.forward_step(4)
                return await responses.request_request(ticket_number)
        else:
            await ticket.create_client_ticket()
            ticket_number = await ticket.get_client_ticket()
            await conversation.forward_step(4)
            return await responses.request_request(ticket_number)

    # Step 3.1 = Confirma tratativa
    elif conversation_step == 3.1:
        r = await check_yes(message_content)
        if r is None:
            return await responses.invalid_bool()
        elif r is False:
            await conversation.forward_step(4)
            return await responses.request_request()
        elif r is True:
            client_request = await ticket.get_request()
            if client_request == "estorno":
                await conversation.forward_step(7)
                return await responses.request_pix_key()
            else:
                if client_chart_list := await ticket.get_chart_list():
                    await conversation.forward_step(5.1)
                    return await responses.request_chart_confirm(client_chart_list)
                else:
                    await conversation.forward_step(5)
                    return await responses.request_chart_list()

    # Step 4 = Recebe o `request`
    elif conversation_step == 4:
        r, option = await check_request_options(message_content)
        if r:
            await ticket.set_client_request(option)
            if int(option) == 1:
                if client_chart_list := await ticket.get_chart_list():
                    await conversation.forward_step(5.1)
                    return await responses.request_chart_confirm(client_chart_list)
                else:
                    await conversation.forward_step(5)
                    return await responses.request_chart_list()
            elif int(option) == 2:
                await conversation.forward_step(7)
                return await responses.request_pix_key()
        else:
            return await responses.invalid_option()

    # Step 5 = Pergunta se o carrinho está correto
    elif conversation_step == 5:
        await ticket.set_chart(message_content)
        await conversation.forward_step(5.1)
        return await responses.request_chart_confirm(message_content)

    # Step 5 = Salva o carrinho
    elif conversation_step == 5.1:
        r = await check_yes(message_content)
        if r is None:
            return await responses.invalid_bool()
        elif r is False:
            await conversation.forward_step(5)
            return await responses.request_chart_list()
        elif r is True:
            if client_seller := await ticket.get_seller():
                await conversation.forward_step(6.1)
                return await responses.request_seller_confirm(client_seller)
            else:
                await conversation.forward_step(6)
                return await responses.request_seller()

    elif conversation_step == 6:
        await ticket.set_seller(message_content)
        r = await check_yes(message_content)
        if r is False:
            client_request = await ticket.get_request()
            if client_request == "estorno":
                await conversation.forward_step(7)
                return await responses.request_pix_key()
            else:
                await _send_mail(client, ticket)
                await conversation.close()
                return await responses.closure()
        else:
            await conversation.forward_step(6.1)
            return await responses.request_seller_confirm(message_content)

    elif conversation_step == 6.1:
        r = await check_yes(message_content)
        if r is None:
            return await responses.invalid_bool()
        elif r is False:
            await conversation.forward_step(6)
            return await responses.request_seller()
        elif r is True:
            client_request = await ticket.get_request()
            if client_request == "estorno":
                await conversation.forward_step(7)
                return await responses.request_pix_key()
            else:
                await _send_mail(client, ticket)
                await conversation.close()
                return await responses.closure()

    elif conversation_step == 7:
        await ticket.set_pix_key(message_content)
        await conversation.forward_step(7.1)
        return await responses.request_pix_confirm(message_content)

    elif conversation_step == 7.1:
        r = await check_yes(message_content)
        if r is None:
            return await responses.invalid_bool()
        elif r is False:
            await conversation.forward_step(7)
            return await responses.request_pix_key()
        elif r is True:
            await _send_mail(client, ticket)
            await conversation.close()
            return await responses.closure()

async def _send_mail(client, ticket):
    client_name = await client.get_name()
    client_email = await client.get_email()
    client_ticket = await ticket.get_client_ticket()
    client_document = await client.get_document()
    client_phone = await client.get_phone()
    client_chart = await ticket.get_chart_list()
    client_request = await ticket.get_request()
    client_seller = await ticket.get_seller()
    subject = f"Protocolo: {client_ticket} ({client_name}) - "
    sent_body_byhi = """Nome completo: %s
        CPF: %s
        Telefone: %s
        Pedido: %s
        Protocolo: %s
        Solicitação: %s
        Vendedor: %s""" % (client_name, client_document, client_phone, client_chart, client_ticket, client_request, client_seller)
    if await ticket.get_request() == "produto":
        sent_body = """Olá, %s.
        Obrigado pelo contato e por enviar as informações pelo nosso SAC!
        O seu protocolo é %s.
        Já coletamos suas informações, porém precisamos que siga os passos abaixo.
        Responda este email com os seguintes anexos:
        1) Comprovantes das compras (Pix ou cartão de crédito)
        2) Envie seu endereço completo com CEP, cidade e estado.
        Pedimos desculpas por qualquer de incoveniencia que possamos ter causado.
        Estamos comprometidos a entender e dar tratativa ao seu caso o mais rápido possível.
        Estamos melhorando nosso sistema de atendimento e reestruturando nossa empresa parar melhor te atender.
        Ficamos no aguardo das informações.
        Agradecemos a atenção!
        SAC ByHi.
        """ % (client_name, client_ticket, )
        mail.send_email([client_email, "byhisac@gmail.com"], f"{subject} Envio pendente SAC BYHI", sent_body)
        mail.send_email(["byhisac@gmail.com"], f"{subject} Envio pendente SAC BYHI - DADOS", sent_body_byhi)
    elif await ticket.get_request() == "estorno":
        sent_body = """Olá, %s.
        Obrigado pelo contato e por enviar as informações pelo nosso SAC!
        O seu protocolo é %s.
        Já coletamos suas informações, porém precisamos que siga os passos abaixo.
        Responda este email com os seguintes anexos:
        1) Comprovantes das compras (Pix ou cartão de crédito)
        Pedimos desculpas por qualquer de incoveniencia que possamos ter causado.
        Estamos comprometidos a entender e dar tratativa ao seu caso o mais rápido possível.
        Estamos melhorando nosso sistema de atendimento e reestruturando nossa empresa parar melhor te atender.
        Ficamos no aguardo das informações.
        Agradecemos a atenção!
        SAC ByHi.
        """ % (client_name, client_ticket, )
        mail.send_email([client_email, "byhisac@gmail.com"], f"{subject} Reembolso SAC BYHI", sent_body)
        mail.send_email(["byhisac@gmail.com"], f"{subject} Reembolso SAC BYHI - DADOS", sent_body_byhi)


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto('https://web.whatsapp.com')

        await asyncio.sleep(10)
        await page.screenshot(path="test.png")
        print("print tirado - qr code")

        await page.wait_for_selector('.tt8xd2xn', timeout=0)

        await page.screenshot(path="test.png")
        print("print tirado - logado")

        await page.wait_for_selector(".tt8xd2xn.bugiwsl0.mpdn4nr2.fooq7fky")
        await page.locator(".tt8xd2xn.bugiwsl0.mpdn4nr2.fooq7fky").click()

        await page.wait_for_selector(".jScby.Iaqxu.FCS6Q")
        filter_options = await page.query_selector_all(".jScby.Iaqxu.FCS6Q")
        await filter_options[0].click()

        await asyncio.sleep(3)
        await page.screenshot(path="test.png")
        print("print tirado - unreadchats")

        while True:
            try:
                print("checando")
                await check_unread_messages(page)
                # Aguarde um tempo antes de verificar novamente
                await asyncio.sleep(2)  # Altere o intervalo de verificação conforme necessário
            except Exception as e:
                traceback.print_exc()
                print(sys.exc_info())
                await page.keyboard.press('Escape')

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())