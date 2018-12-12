# Belgar's Code :)

from message import IRC_Message

class IRC_User():

    count = 0

    def __init__(self, data: str):
        ## data = user mask
        self.id = IRC_User.count
        IRC_User.count += 1

        self.nick, data = data.split("!")
        self.ident, self.ident = data.split("@")

        self.register = False
        self.online = True
        self.ipv = None

        ## Lista de IRC_Users IDs Relacionados
        self.aliases = []

        self.messages = {}

        ## Seguimiento de cambios de nick... registrados no registrados... alias, clones, ...


    def add_message(self, message: IRC_Message):
        self.messages[message.id] = message

    def __format__(self, format):
        if (format == 'id'):
            return '{}'.format(self.id)
        if (format == 'nick'):
            return '{}'.format(self.nick)
        if (format == 'mask'):
            return '{}!{}@{}'.format(self.nick, self.ident, self.ipv)
        if (format == 'messages'):
            return '{}'.format(len(self.messages))
        if (format == 'long'):
            if self.online: online = "Conectado"
            else: online = "Desconectado"
            if self.register: register = "Registrado"
            else: register = "No Registrado"
            return '{} esta {}, {}, tiene {} alias y ha puesto {} Mensages'.format(self.nick, online, register, len(self.aliases), len(self.messages))
        return 'IRC_User'
