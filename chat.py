#!/var/env/chat/bin/python3.7
# Belgar's Code :)

import asyncio
from irc_proto import IRC_Client_Protocol

async def chat(server: str):
    loop = asyncio.get_running_loop()

    while True:
        on_lost = loop.create_future()
        transport, protocol = await loop.create_connection( lambda: IRC_Client_Protocol(loop, on_lost), server, 6697, ssl=True)
        await on_lost


if __name__ == "__main__":
    asyncio.run(chat("irc.chathispano.com"))
