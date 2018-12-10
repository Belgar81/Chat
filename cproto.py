import asyncio
from message import IRC_Message
from channel import IRC_Channel
from user import IRC_User

class IRC_Client_Protocol(asyncio.BufferedProtocol):

    def __init__(self, on_lost, loop, channel):
        self.loop = loop
        self.buffer: bytearray = None
        self.transport = None
        self.on_lost = on_lost
        self.lastmessage = None
        self.isConnected = False

        self.server = { 'name': None, 'messages':[]}
        self.channel = IRC_Channel(channel)
        self.users = {'SynoBot':IRC_User("SynoBot!SynoBot@DdAbcZ.BUtNt6.virtual")}

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
                        message = IRC_Message(line.splitlines()[0], self.server["name"])
                        self.dispatcher(message)
        return None

    def eof_received(self) -> None:
        print ('Conexion Cerrada.')
        self.on_lost.set_result(True)

    def dispatcher(self, message: IRC_Message):

        print ('{:long}'.format(message))

        if (message.command["value"] == "MODE"):
            self.write('JOIN {:long} \r\n'.format(self.channel))
            self.write('MODE SynoBot +c\r\n')


        if (message.prefix["type"] != "user"): return

        if (message.command["type"] != "long"): return

        if (message.command["value"] == "PRIVMSG"):
            nick = message.prefix["value"].strip('!')[0]
            if nick in self.users.keys():

                self.users[nick].messages.append(message)

                if (message.params["trailing"] == ".users"):
                    out = 'PRIVMSG {:long} :'.format(self.channel)
                    for user in self.users.values():
                        out += '{:long}; '.format(user)
                    out += "\r\n"
                    self.write(out)

        if (message.command["value"] == "JOIN"):
            nick = message.prefix["value"].split("!")[0]
            if nick in self.users.keys():
                self.users[nick].inside = True
            else:
                user = IRC_User(message.prefix["value"])
                user.inside = True
                self.users[user.nick] = user
                print ('{:long}'.format(user))

        for cmd in ["PART", "QUIT"]:
            if (message.command["value"] == cmd):
                nick = message.prefix["value"].split("!")[0]
                if nick in self.users.keys():
                    self.users[nick].inside = False
