import asyncio
from message import IRC_Message
from channel import IRC_Channel

class IRC_Client_Protocol(asyncio.BufferedProtocol):

    def __init__(self, on_lost, loop):
        self.loop = loop
        self.buffer: bytearray = None
        self.transport = None
        self.on_lost = on_lost
        self.lastmessage = None
        self.isConnected = False

        self.server = {'name': None, 'messages':[], 'channels':[IRC_Channel("#barcelona_liberal")]}

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
                if not self.server["name"]:
                    self.server["name"] = line.split()[0][1:]
                if (line[:4] == 'PING'):
                    self.isConnected = True
                    self.write('PONG' + line[4:])
            else:
                if (line[-1:] != '\n'): self.lastmessage = line
                else:
                    if self.lastmessage:
                        line = self.lastmessage + line
                        self.lastmessage = None
                    if (line[:4] == 'PING'):
                        self.write('PONG' + line[4:])
                    else:
                        message = IRC_Message(line.splitlines()[0], self.server["name"])
                        self.dispatcher(message)
        return None

    def eof_received(self) -> None:
        print('The server closed the connection')
        self.on_lost.set_result(True)

    def dispatcher(self, message: IRC_Message):

        print (message)

        if (message.command["value"] == "MODE"):
            self.write("JOIN #barcelona_liberal\r\n")

#:barnamen_!android@BJVCHj.BrTPIQ.virtual JOIN :#barcelona_liberal

        #if message.prefix["isServer"]:
        #    self.server["messages"].append(message)
