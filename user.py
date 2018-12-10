class IRC_User():

    def __init__(self):
        self.nick = None
        self.ident = None
        self.ipv = None
        self.modes = None
        self.online = False

        self.messages = []
