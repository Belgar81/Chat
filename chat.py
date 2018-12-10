#!/var/env/chat/bin/python3.7
# Belgar's Code :)

import asyncio
import signal
import functools
import argparse
from cproto import IRC_Client_Protocol

async def chat(server: str, channel: str):
    loop = asyncio.get_running_loop()

    while True:
        on_lost = loop.create_future()
        transport, protocol = await loop.create_connection( lambda: IRC_Client_Protocol(loop, on_lost, channel), server, 6697, ssl=True)
        await on_lost


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='IRC Protocol PoC')
    parser.add_argument('server', metavar='server', type=str, help='IRC Server FDQN')
    parser.add_argument('channel', metavar='channel', type=str, help='IRC Channel with #')
    args = parser.parse_args()

    asyncio.run(chat(vars(args)["server"], vars(args)["channel"]))
