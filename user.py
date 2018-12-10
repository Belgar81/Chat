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
        if (format == 'long'):
            return '{}) {} tiene {} Mensages'.format(self.id, self.nick, len(self.messages))
        if (format == 'mask'):
            return '{}!{}@{}'.format(self.nick, self.ident, self.ipv)
        if (format == 'nick'):
            return '{}'.format(self.nick)
        return 'IRC_User'
