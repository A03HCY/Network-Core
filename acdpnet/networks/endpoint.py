from acdpnet.protocol import *

import socketserver as sksv
import threading    as td
import socket



class Endpoint:
    def __init__(self, save:bool=False):
        self.ok = False
        self.func = {}
        self.save = save
        self.__gene__()

    def __gene__(self):
        for n in dir(self):
            if not n.startswith('on_'): continue
            self.__regs__('.' + n[3:], getattr(self, n))

    def __regs__(self, extn, func, **options):
        self.func[extn] = [func, options]
    
    def __result__(self, head:str, data:Protocol):
        func = self.func[head][0]
        resl = func(data)
        if type(resl) == Protocol:
            self.net.multi_push(data)
            print('pushed', self.net.pool)

    def __hadl__(self, data:Protocol):
        print('Gate', data)
        head, extn = Autils.chains(data.extn)
        head = '.' + head
        if head in self.func:
            thread = td.Thread(target=self.__result__, args=(head, data,))
            thread.start()
        return not self.save

    def route(self, extn, **options):
        if not extn[0] == '.': extn = '.' + extn
        def regsfunc(func):
            self.__regs__(extn, func, **options)
            return func
        return regsfunc
    
    def setnet(self, net:Acdpnet):
        self.net = net
        self.ok = True
        return self
    
    def run(self):
        if not self.ok: raise EnvironmentError('Network was not set')
        self.net.recv_func = self.__hadl__
        self.net.auto_start(wait=True)


def Generate(data_handler:dict, tp:str='TCP'):
    class Gate(sksv.BaseRequestHandler):
        def __init__(self, *args):
            self.data_handler = data_handler
            self.tp = tp
            super().__init__(*args)
        def setup(self):
            print('one in')
        def handle(self):
            net = Acdpnet().setio(read=self.request.recv, write=self.request.send)
            end = Endpoint().setnet(net)
            end.func = self.data_handler
            end.run()
        def finish(self):
            print('one out')
    return Gate


class SocketPiont(Endpoint):
    def setnet(self, host:str, port:int):
        self.host = host
        self.port = port
        self.ok   = True
        return self
    
    def run(self):
        if not self.ok: raise EnvironmentError('Network was not set')
        sksv.TCPServer((self.host, self.port), Generate(self.func)).serve_forever()


class SocketTerminal(Endpoint):
    def setnet(self, host:str, port:int):
        self.host = host
        self.port = port
        self.ok   = True
        self.sk   = socket.socket()
        return self

    def connect(self):
        if not self.ok: raise EnvironmentError('Network was not set')
        self.sk.connect((self.host, self.port))
        self.net = Acdpnet().setio(read=self.sk.recv, write=self.sk.send)
        self.net.recv_func = self.__hadl__
        self.net.auto_start()

    def send(self, data:Protocol):
        print('sd', data)
        self.net.multi_push(data)
    
    def close(self):
        self.sk.close()

    def keep(self):
        self.net.recv_thread.join()
        self.net.send_thread.join()