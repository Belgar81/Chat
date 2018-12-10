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

    def reload(self, data: str):
        self.ident, self.ipv = data.split("!")[1].split("@")

    def get_count(self):
        return (IRC_User.count)

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
            if self.inside: online = "Conectado"
            else: online = "Desconectado"
            return '{} esta {} y tiene {} Mensages'.format(self.nick, online, len(self.messages))
        return 'IRC_User'
