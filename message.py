class IRC_Message():

    def __init__(self, data: str, servername: str):
        
        self.prefix = {'isServer':True, 'value':None}
        self.command = {'isServer':True, 'value':None}
        self.params = {'middle':[], 'trailing':None}

        self.prefix["value"], self.command["value"], data = data[1:].split(maxsplit=2)
        if (self.prefix["value"] != servername): self.prefix["isServer"] = False
        self.command["value"].lstrip()
        if not self.command["value"].isdigit(): self.command["isServer"] = False
        data.lstrip()

        while (data[0] != ":"):
            try:
                m, data = data.split(maxsplit=1)
                self.params["middle"].append(m)
                data[0].lstrip()
            except ValueError:
                self.params["middle"].append(data)
                data = [":"]

        if (len(data) > 1):
            self.params["trailing"] = ''.join(data[1:])

    def __str__(self):
        return "=> " + str(self.prefix["value"]) + " " + str(self.command["value"]) + " " + str(self.params)
