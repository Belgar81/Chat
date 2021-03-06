# Belgar's Code :)

import asyncio
from server import IRC_Server

class IRC_Client_Protocol(asyncio.BufferedProtocol):

    def __init__(self, on_lost, loop):
        self.loop = loop
        self.buffer: bytearray = None
        self.transport = None
        self.on_lost = on_lost
        self.lastmessage = None
        self.isConnected = False


        self.server = IRC_Server()

        #actions

    def connection_made(self, transport):
        self.transport = transport
        self.transport.write('USER SynoBot * * :SynoBot\r\n'.encode())
        self.transport.write('NICK SynoBot\r\n'.encode())

    def get_buffer(self, size: int) -> bytearray:
        self.buffer = bytearray(4096)
        return self.buffer

    def write(self, message):
        self.transport.write(message.encode())

    def buffer_updated(self, nbytes: int) -> None:

        lines = self.buffer[:nbytes].splitlines(True)

        for line in lines:

            line = line.decode(errors='replace')

            if not self.isConnected:
                self.server.add_server(line.split()[0][1:])

                if (line[:4] == 'PING'):
                    self.isConnected = True
                    self.write('PONG{}'.format(line[4:]))
            else:
                if (line[-1:] != '\n'): self.lastmessage = line
                else:
                    if self.lastmessage:
                        line = self.lastmessage + line
                        self.lastmessage = None
                    if (line[:4] == 'PING'):
                        self.write('PONG{}'.format(line[4:]))
                    else:
                        self.dispatcher(line)
        return None

    def eof_received(self) -> None:
        print ('Conexion Cerrada.')
        self.on_lost.set_result(True)


    def dispatcher(self, data: str):

        action = self.server.add_message(data)
        if action: self.write(action)
