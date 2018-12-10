from message import IRC_Message
from user import IRC_User

class IRC_Channel():

    def __init__(self, name: str):
        self.name = name
        self.modes = None
        self.users = {}

    def dispatcher(self, message: IRC_Message):

        if (message.command["value"] == "379"):
            print ("MODES: ")

            nick = message.params["middle"][1]
            if nick in self.users.keys(): user = self.users[nick]
            else: return None

            print (message.params["trailing"].split()[-1:][0])
            if 'r' in message.params["trailing"].split()[-1:][0]:
                user.identity["register"] = True
            else:
                user.identity["register"] = False
            return None

        if ((message.prefix["type"] == "user") and (message.command["type"] == "long")):
            nick = message.prefix["value"].split("!")[0]

            if nick in self.users.keys():

                user = self.users[nick]

                if (message.command["value"] == "PRIVMSG"):

                    print ('PRIVMSG: {:long} :'.format(user))

                    user.messages.append(message)

                    if (message.params["trailing"] == ".usuarios"):
                        return 'PRIVMSG {} : Hay {} usuarios en la Base de Datos\r\n'.format(self.name, user.get_count())

                    if (message.params["trailing"] == ".yo"):
                        return 'PRIVMSG {:long} :\r\n'.format(user)

                if (message.command["value"] == "JOIN"):
                    print ("JOIN: ")
                    user.join(message.prefix["value"])
                    return None

                for cmd in ["PART", "QUIT"]:
                    if (message.command["value"] == cmd):
                        print ("PART/QUIT: ")
                        user.quit()
                        return None
            else:
                if (message.command["value"] == "JOIN"):
                    self.users[nick] = IRC_User(message.prefix["value"])
                    print ('REGISTER: {:long}'.format(self.users[nick]))
                    return 'WHOIS {}\r\n'.format(nick)

        return None



    def __format__(self, format):
        if (format == 'name'):
            return '{}'.format(self.name)
        return 'IRC_Channel'
