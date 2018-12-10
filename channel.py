class IRC_Channel():

    def __init__(self, name: str):
        self.name = name
        self.modes = None

    def __format__(self, format):
        if (format == 'long'):
            return '{}'.format(self.name)
        return 'IRC_Channel'
