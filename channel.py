# Belgar's Code :)

from message import IRC_Message

class IRC_Channel():

    count = 0

    def __init__(self, name: str):
        self.id = IRC_Channel.count
        IRC_Channel.count += 1

        self.name = name
        self.modes = None
        self.users = {}
        self.messages = []

    def add_message(self, message: IRC_Message):

        pass



    def __format__(self, format):
        if (format == 'name'):
            return '{}'.format(self.name)
        return 'IRC_Channel'
