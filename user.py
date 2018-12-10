class IRC_User():

    count = 0

    def __init__(self, data: str):
        self.id = IRC_User.count
        self.nick, data = data.split("!")
        self.ident, self.ipv = data.split("@")
        self.modes = None
        self.inside = False
        self.messages = []

        IRC_User.count += 1

    def __format__(self, format):
        if (format == 'nick'):
            return '{}'.format(self.nick)
        if (format == 'mask'):
            return '{}!{}@{}'.format(self.nick, self.ident, self.ipv)
        if (format == 'long'):
            if self.inside: online = "Conectado"
            else: online = "Desconectado"
            return '{} esta {} y tiene {} Mensages'.format(self.nick, online, len(self.messages))
        return 'IRC_User'
