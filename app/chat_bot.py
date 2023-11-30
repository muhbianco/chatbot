import asyncio
import re
from dotenv import load_dotenv
from pprint import pformat
from playwright.async_api import async_playwright
from pycpfcnpj import cpfcnpj

from utils.db import DB
from utils.helpers import *
from utils.bot_responses import BotResponses

from classes.conversation import Conversation
from classes.client import Client

db = DB()
responses = BotResponses()


async def check_unread_messages(page):
    # Pegue todas as conversas não lidas
    unread_chats = await page.query_selector_all('.aumms1qt')

    if unread_chats:
        # Se houver mensagens não lidas, clique na primeira
        await unread_chats[0].click()

        # Aguarde um momento para a mensagem ser carregada
        await page.wait_for_timeout(2000)

        # Abre o contact info
        await page.locator(".AmmtE span[data-icon='menu']").click()
        await page.locator("div[aria-label='Contact info']").click()

        await asyncio.sleep(5)
        await page.screenshot(path="test.png")
        print("print tirado - contact info")

        # Coleta o numero de telefone do cliente
        contact_number = await page.locator(".q9lllk4z.e1gr2w1z.qfejxiq4").inner_text()
        if not await valid_phone_number(contact_number):
            contact_number = await page.locator(".enbbiyaj.e1gr2w1z.hp667wtd").inner_text()

        await page.locator("div[aria-label='Close'] span[data-icon='x']").click()
        await asyncio.sleep(1)

        # Pega a ultima mensagem enviada pelo cliente
        messages = await page.query_selector_all('.message-in')
        last_message_content = await messages[len(messages)-1].text_content()

        split_message = re.split(r"(AM|PM)", last_message_content.strip())
        last_message_content = split_message[0].replace(split_message[2], "")
        if not last_message_content:
            response = await responses.general_error()

        response = await message_treatment(page, contact_number, last_message_content)
        place_holder = page.get_by_title("Type a message")
        await place_holder.focus()
        await place_holder.type(response)
        await page.locator("button[aria-label='Send']").click()
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

    # Step 1 = Consulta o CPF da table clients
    # Cria o contato e solicita o Nome completo
    if await conversation.step() == 1:
        document = await strip_document(message_content)
        client = Client(document, contact_number)
        await conversation.set_document(document)

        if cpfcnpj.validate(document):
            if not await client.is_exists():
                client_id = await client.create_client()
                await conversation.forward_step(2)
                return await responses.request_name()
            else:
                client_name = await client.get_name()
                if client_name:
                    await conversation.forward_step(1.1)
                    return await responses.confirm_name(client_name)
                else:
                    await conversation.forward_step(2)
                    return await responses.request_name()
        else:
            return await responses.invalid_document()

    # Step 1.1 = Trata a resposta confirmação do nome existente
    elif await conversation.step() == 1.1:
        r = await check_yes(message_content)
        if r is None:
            return await responses.invalid_bool()
        elif r is False:
            await conversation.forward_step(2)
            return await responses.request_name_change()
        elif r is True:
            client_email = await client.get_email()
            if client_email:
                await conversation.forward_step(2.1)
                return await responses.confirm_email(client_email)
            else:
                await conversation.forward_step(3)
                return await responses.request_email()

    # Step 2 = Salva o nome informado e solicita o email
    elif await conversation.step() == 2:
        await client.set_name(message_content)
        client_email = await client.get_email()
        if client_email:
            await conversation.forward_step(2.1)
            return await responses.confirm_email(client_email)
        else:
            await conversation.forward_step(3)
            return await responses.request_email()

    # Step 2.1 = Trata a resposta confirmação do email existente
    elif await conversation.step() == 1.1:
        r = await check_yes(message_content)
        if r is None:
            return await responses.invalid_bool()
        elif r is False:
            await conversation.forward_step(3)
            return await responses.request_email_change()
        elif r is True:
            await conversation.forward_step(4)
            return "Certo, o que deseja?"

    # Step 3 = Recebe o email
    elif await conversation.step() == 3:
        await client.set_email(message_content)
        await conversation.forward_step(4)
        return "Certo, o que deseja?"



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

        await page.locator("button[aria-label='Unread chats filter']").click()        

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
                print("Reiniciando", str(e))
                await page.keyboard.press('Escape')

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())