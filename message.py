# Belgar's Code :)

import time

class IRC_Message():

    def __init__(self):
        self.id = time.time()

        self.prefix = {'type':None, 'value':None}
        #types: server, user, misc
        self.command = {'type':None, 'value':None}
        #types: short, long
        self.params = {'middle':[], 'trailing':None}

    def dispatcher(self):

        if (self.command["value"] == "376"):
            ## {'type': 'server', 'value': 'ganimedes.chathispano.com'}
            ## {'type': 'short', 'value': '376'}
            ## {'middle': ['SynoBot'], 'trailing': 'End of /MOTD command\r\n'}
            return '{}:'.format("bootjoin")

        if (self.command["value"] == "379"):
            ## {'type': 'server', 'value': 'miranda.chathispano.com'} =>
            ##
            ##  {'type': 'short', 'value': '319'} =>
            ##      {'middle': ['SynoBot', 'sabadellparcatalunya'], 'trailing': '#barcelona_liberal \r\n'}
            ##
            ##  {'type': 'short', 'value': '312'} =>
            ##      {'middle': ['SynoBot', 'sabadellparcatalunya', 'irc.chathispano.com'],
            ##      'trailing': 'Servidor de ChatHispano\r\n'}
            ##
            ##  {'type': 'short', 'value': '379'} =>
            ##      {'middle': ['SynoBot', 'sabadellparcatalunya'], 'trailing': 'Utiliza los modos [x]\r\n'}
            nick = self.params["middle"][1]
            modes = self.params["trailing"].split()[-1:][0]
            return '{}:{}:{}'.format("379", nick, modes)

        if (self.command["value"] == "311"):
            ## {'type': 'server', 'value': 'miranda.chathispano.com'} =>
            ## {'type': 'short', 'value': '311'} =>
            ## {'middle': ['SynoBot', 'sabadellparcatalunya', 'ircap', 'C70IDD.Ck4MvN.virtual', '*'],
            ##  'trailing': 'IRcap[8.72] \x037\x02\x07\x0f www.ircap.com\r\n'}
            nick, ident, ipv = self.params["middle"][1:4]
            return '{}:{}:{}:{}'.format("311", nick, ident, ipv)

        if (self.command["value"] == "318"):
            ## {'type': 'server', 'value': 'miranda.chathispano.com'} =>
            ## {'type': 'short', 'value': '318'} =>
            ## {'middle': ['SynoBot', 'sabadellparcatalunya'], 'trailing': 'End of /WHOIS list
            nick = self.params["middle"][1]
            return '{}:{}'.format("318", nick)

        if ((self.prefix["type"] == "user") and (self.command["type"] == "long")):

            nick = self.prefix["value"].split("!")[0]

            if (self.command["value"] == "JOIN"):
                ## {'type': 'long', 'value': 'JOIN'} => {'middle': [], 'trailing': '#barcelona_liberal\r\n'}
                channel = self.params["trailing"].splitlines()[0]
                return '{}:{}:{}'.format("join", nick, channel)
            elif (self.command["value"] == "PART"):
                ## {'type': 'long', 'value': 'PART'} => {'middle': ['#barcelona_liberal\r\n'], 'trailing': None}
                channel = self.params["middle"][0].splitlines()[0]
                return '{}:{}:{}'.format("part", nick, channel)
            elif (self.command["value"] == "QUIT"):
                ## {'type': 'long', 'value': 'QUIT'} => {'middle': [], 'trailing': 'Ping timeout\r\n'}
                return '{}:{}'.format("quit", nick)
            elif (self.command["value"] == "NICK"):
                ## {'type': 'long', 'value': 'NICK'} => {'middle': [], 'trailing': 'FeiT0\r\n'}
                newnick = self.params["trailing"].splitlines()[0]
                return '{}:{}:{}'.format("nick", nick, newnick)
            elif (self.command["value"] == "PRIVMSG"):
                ## {'type': 'long', 'value': 'PRIVMSG'} => {'middle': ['#barcelona_liberal'], 'trailing': 'Anonimaa buenas\r\n'
                channel = self.params["middle"][0]
                message = self.params["trailing"].splitlines()[0]
                return '{}:{}:{}:{}'.format("privmsg", nick, channel, message)

            else: return False

        return None


    def __format__(self, format):
        if (format == 'long'):
            return '{} => {} => {} => {}'.format((time.asctime(time.localtime(self.id))),self.prefix, self.command, self.params)
            return 'IRC_Message'
