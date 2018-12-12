# Belgar's Code :)

from message import IRC_Message

class IRC_User():

    count = 0

    def __init__(self, data: str):
        ## data = user mask
        self.id = IRC_User.count
        IRC_User.count += 1

        self.identity = {'nick':None, 'ident':None, 'register':False, 'online':True, 'ipv':None, 'olds_ipvs': []}
        self.alias = []

        self.identity["nick"], data = data.split("!")
        self.identity["ident"], self.identity["ipv"] = data.split("@")

        self.messages = {}

        #print (self.identity)

        ## Seguimiento de cambios de nick... registrados no registrados... alias, clones, ...


    def add_message(self, message: IRC_Message):
        self.messages[message.id] = message

    def __format__(self, format):
        if (format == 'id'):
            return '{}'.format(self.id)
        if (format == 'nick'):
            return '{}'.format(self.identity["nick"])
        if (format == 'mask'):
            return '{}!{}@{}'.format(self.identity["nick"], self.identity["ident"], self.identity["ipv"])
        if (format == 'messages'):
            return '{}'.format(len(self.messages))
        if (format == 'long'):
            if self.identity["online"]: online = "Conectado"
            else: online = "Desconectado"
            if self.identity["register"]: register = "Registrado"
            else: register = "No Registrado"
            return '{} esta {}, {} y ha puesto {} Mensages'.format(self.identity["nick"], online, register, len(self.messages))
        return 'IRC_User'
