from sys import platform

if platform == 'win32':
    from speclenium_win32 import Speclenium
else:
    from speclenium_atspi import Speclenium

def main(port=4117):
    from twisted.internet import reactor
    from twisted.web import server
    r = Speclenium()
    reactor.listenTCP(port, server.Site(r))
    reactor.run()
