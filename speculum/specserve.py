from sys import platform

if platform == 'win32':
    from specserve_win32 import SpecServe
else:
    from specserve_atspi import SpecServe
    
if __name__ == '__main__':
    from twisted.internet import reactor
    from twisted.web import server
    r = SpecServe()
    reactor.listenTCP(7080, server.Site(r))
    reactor.run()
