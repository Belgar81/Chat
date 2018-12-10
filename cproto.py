import asyncio
from message import IRC_Message

class IRC_Client_Protocol(asyncio.BufferedProtocol):

    def __init__(self, on_lost, loop):
        self.loop = loop
        self.buffer: bytearray = None
        self.transport = None
        self.on_lost = on_lost
        self.servername = None
        self.lastmessage = None
        self.isConnected = False

    def connection_made(self, transport):
        self.transport = transport
        self.transport.write('USER SynoBot * * :SynoBot\r\n'.encode())
        self.transport.write('NICK SynoBot\r\n'.encode())

    def get_buffer(self, size: int) -> bytearray:
        self.buffer = bytearray(4096)
        return self.buffer

    def write(self, message):
        print("WRITE: " + message)
        self.transport.write(message.encode())

    def buffer_updated(self, nbytes: int) -> None:

        lines = self.buffer[:nbytes].splitlines(True)

        for line in lines:

            line = line.decode(errors='replace')

            print (line)

            if not self.isConnected:
                if not self.servername:
                    self.servername = line.split()[0][1:]
                if (line[:4] == 'PING'):
                    self.isConnected = True
                    self.write('PONG' + line[4:])
            else:
                if (line[-1:] != '\n'): self.lastmessage = line
                else:
                    if self.lastmessage:
                        line = line + self.lastmessage
                        self.lastmessage = None
                    if (line[:4] == 'PING'):
                        self.write('PONG' + line[4:])
                    else:
                        message = IRC_Message(line, self.servername)
                        if (message.command["value"] == "MODE"):
                            self.write("JOIN #barcelona_liberal\r\n")

        return None

    def eof_received(self) -> None:
        print('The server closed the connection')
        self.on_lost.set_result(True)
