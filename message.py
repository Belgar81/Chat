import re
import time

re_usermask = ("^\S+\!\S+\@\S+")

class IRC_Message():

    def __init__(self, data: str, servername: str):

        self.prefix = {'type':None, 'value':None}
        #types: server, user, misc
        self.command = {'type':"long", 'value':None}
        #types: short, long
        self.params = {'middle':[], 'trailing':None}
        self.timestamp = time.time()

        self.prefix["value"], self.command["value"], data = data[1:].split(maxsplit=2)
        if (self.prefix["value"] == servername): self.prefix["type"] = "server"
        elif re.match(re_usermask, self.prefix["value"]): self.prefix["type"] = "user"
        else: self.prefix["type"] = "misc"
        self.command["value"].lstrip()
        if self.command["value"].isdigit(): self.command["type"] = "short"
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

    def __format__(self, format):
        if (format == 'long'):
            return '{:10.2f} => {}: {} => {}: {} => {}'.format(self.timestamp, self.prefix["type"],
                    self.prefix["value"], self.command["type"], self.command["value"], self.params)
        return 'IRC_Message'
