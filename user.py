class IRC_User():

    def __init__(self, data: str):
        self.nick, data = data.split("!")
        self.ident, self.ipv = data.split("@")
        self.modes = None
        self.inside = False

        self.messages = []
