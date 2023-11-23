import asyncio
import re
from dotenv import load_dotenv
from pprint import pformat
from playwright.async_api import async_playwright

from utils.db import DB


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
        contact_number = await page.locator(".enbbiyaj.e1gr2w1z.hp667wtd").inner_text()
        await page.locator("div[aria-label='Close'] span[data-icon='x']").click()

        # Pega a ultima mensagem enviada pelo cliente
        messages = await page.query_selector_all('.message-in')
        last_message_content = await messages[len(messages)-1].text_content()
        last_message_content = (
            re.sub(r'\d+:\d+\s\w+', '', last_message_content)
            .strip()
            .split(":")[0]
            .strip()
        )

        await message_treatment(page, contact_number, last_message_content)

        place_holder = page.get_by_title("Type a message")
        await place_holder.focus()
        await place_holder.type("Teste de resposta automática.")

        await page.locator("button[aria-label='Send']").click()

    else:
        print('Não há mensagens não lidas.')


async def message_treatment(page, contact_number, message_content, db=DB()):
    print("contact_number:::::::", contact_number)
    print("message_content:::::::", message_content)
    print(await db.fetchone("select * from clients"))

async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto('https://web.whatsapp.com')

        await asyncio.sleep(10)
        await page.screenshot(path="test.png")
        print("print tirado - qr code")

        await page.wait_for_selector('.tt8xd2xn')

        await page.screenshot(path="test.png")
        print("print tirado - logado")

        await page.locator("button[aria-label='Unread chats filter']").click()        

        await asyncio.sleep(10)
        await page.screenshot(path="test.png")
        print("print tirado - unreadchats")

        while True:
            print("checando")
            await check_unread_messages(page)
            # Aguarde um tempo antes de verificar novamente
            await asyncio.sleep(5)  # Altere o intervalo de verificação conforme necessário

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())