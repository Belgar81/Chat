# Belgar's Code :)

from message import IRC_Message
from channel import IRC_Channel
from user import IRC_User

import re

re_usermask = ("^\S+\!\S+\@\S+")

class IRC_Server():

    def __init__(self):
        """
            'Id Server' = 'ChatHispano'
            'Servers FQDNs' = 'ganimedes.chathispano.com'

            'Id User' = IRC_User.nick = 'Xiquet24'
            'Alias' = IRC_User.alias   TODO ...

            'Id Misc' = 'ChatHispano'
            'Network Bots' = CHaN!-@-' ...

            TODO: White List Command Messages... to Parser.
        """
        self.servers = { 'ChatHispano': []}
        self.misc = { 'ChatHispano': ['CHaN!-@-']}
        self.users = {}

        self.channel = IRC_Channel("#barcelona_liberal")


    def add_server(self, server: str):
        if server not in self.servers["ChatHispano"]:
            self.servers["ChatHispano"].append(server)

    def add_message(self, data: str):

        message = IRC_Message()

        message.prefix["value"], message.command["value"], data = data[1:].split(maxsplit=2)

        if message.prefix["value"] in self.servers["ChatHispano"]:
            message.prefix["type"] = "server"
        elif message.prefix["value"] in self.misc["ChatHispano"]:
            message.prefix["type"] = "misc"
        elif re.match(re_usermask, message.prefix["value"]):
            message.prefix["type"] = "user"
        else: return False

        message.command["value"].lstrip()
        if message.command["value"].isdigit():
            message.command["type"] = "short"
        else:
            message.command["type"] = "long"

        data.lstrip()

        while (data[0] != ":"):
            try:
                m, data = data.split(maxsplit=1)
                message.params["middle"].append(m)
                data[0].lstrip()
            except ValueError:
                message.params["middle"].append(data)
                data = [":"]

        if (len(data) > 1):
            message.params["trailing"] = ''.join(data[1:])

        """
        self.channel.add_message(message)

        if (message.prefix["type"] == "user"):
            nick = message.prefix["value"]
            if nick in self.users.keys():
                self.users[nick].add_message(message)

        """
        #print ('{:long}'.format(message))



        action = message.dispatcher()

        if not action: return None

        cmd, action = action.split(':', maxsplit=1)

        ## '{}:'.format("bootjoin")
        if (cmd == "bootjoin"):
            return 'JOIN #barcelona_liberal\r\nMODE SynoBot +c\r\n'

        ## '{}:{}:{}'.format("379", nick, modes)
        elif (cmd == "379"):
            nick, modes = action.split(':', maxsplit=1)

            if nick in self.users.keys():
                user = self.users[nick]

                if 'r' in modes:
                    user.register = True
                else:
                    user.register = False

            return None

        ## '{}:{}:{}:{}'.format("311", nick, ident, ipv)
        elif (cmd == "311"):
            nick, ident, ipv = action.split(':', maxsplit=2)
            if (nick not in self.users.keys()):
                self.users[nick] = IRC_User('{}!{}@{}'.format(nick, ident, ipv))
                self.users[nick].online = True
            for u in self.users.values():
                if (ipv == u.ipv):
                    self.users[nick].aliases.append(u.id)
                    u.aliases.append(self.users[nick].id)

        ## '{}:{}'.format("318", nick)
        elif (cmd == "318"):
            nick = action
            if (nick in self.users.keys()):
                print ('{:long}'.format(self.users[nick]))

        ## '{}:{}:{}'.format("join", nick, channel)
        elif (cmd == "join"):
            nick, channel = action.split(':', maxsplit=1)
            if ( channel == self.channel.name):
                if (nick in self.users.keys()):
                    self.users[nick].online = True
                else:
                    return 'WHOIS {}\r\n'.format(nick)
            return None

        ## '{}:{}:{}'.format("part", nick, channel)
        elif (cmd == "part"):
            nick, channel = action.split(':', maxsplit=1)
            if ( channel == self.channel.name):
                if (nick in self.users.keys()):
                    self.users[nick].online = False
                    return None

        ## '{}:{}'.format("quit", nick)
        elif (cmd == "quit"):
            nick = action
            if (nick in self.users.keys()):
                self.users[nick].online = False
                return None

        ## '{}:{}:{}'.format("nick", nick, newnick)
        elif (cmd == "nick"):
            nick, newnick = action.split(':', maxsplit=1)
            if (nick in self.users.keys()):
                self.users[nick].online = False
                if (newnick in self.users.keys()):
                    self.users[nick].aliases.append(self.users[newnick].id)
            if (newnick in self.users.keys()):
                self.users[newnick].online = True
                if (nick in self.users.keys()):
                    self.users[newnick].aliases.append(self.users[nick].id)
            else:
                ## Faltaria relacionar los aliases en este caso...
                ## De momento lo hacemos solo si la ipv coincide de forma simultanea con otros nicks online
                return 'WHOIS {}\r\n'.format(newnick)


        ## '{}:{}'.format("privmsg", nick, channel, message)
        elif (cmd == "privmsg"):
            nick, channel, sms = action.split(':', maxsplit=2)

            if (channel == self.channel.name):
                if (nick in self.users.keys()):
                    self.users[nick].add_message(message)

            if (nick == "Belgar"):
                if ( sms == ".usuarios" ):
                    return 'PRIVMSG {} :Usuarios: {}\r\n'.format("Belgar", self.users.keys())
                elif ( sms.split()[0] == ".user" ):
                    if (sms.split()[1] in self.users.keys()):
                        return 'PRIVMSG {} :{:long} \r\n'.format("Belgar", self.users[sms.split()[1]])
                else: return None
            else: return None

        ## TODO
        else: return None

        return None

        """
            TODO:
                - Modificar la clave de la entrada a IRC_User con el nick Actual. NO.
                - Si hay clones QUE? No sirve. Hay que hacer una clase Abstracta Identidad que relacione todos los Clones.
                - Lista de Canales multiples en mensajes JOIN, PART
        """
