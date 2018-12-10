class IRC_User():

    count = 0

    def __init__(self, data: str):
        self.id = IRC_User.count
        IRC_User.count += 1

        self.identity = {'nick':None, 'ident':None, 'register':False, 'online':True, 'ipv':None, 'olds_ipvs': []}
        self.alias = {'identidad': []}

        self.identity["nick"], data = data.split("!")
        self.identity["ident"], self.identity["ipv"] = data.split("@")

        self.messages = []

        print (self.identity)

        ## Seguimiento de cambios de nick... registrados no registrados... alias, clones, ...

    def join(self, data: str):
        self.identity["online"] = True

    def quit(self):
        self.identity["online"] = False

    def get_count(self):
        return (IRC_User.count)

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
