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


def Generate(data_handler:dict):
    class Gate(sksv.BaseRequestHandler):
        def setup(self):
            print('one in')

        def handle(self):
            net = Acdpnet().setio(read=self.request.recv, write=self.request.send)
            net.debug = True
            self.end = Endpoint().setnet(net)
            self.end.func = data_handler
            self.end.run()
            
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


class SocketTerminal:
    def connect(self, host:str, port:int):
        self.host = host
        self.port = port
        self.ok   = True
        self.sk   = socket.socket()
        self.sk.connect((self.host, self.port))
        self.net  = Acdpnet().setio(self.sk.recv, self.sk.send)
        self.net.debug = True
        self.net.auto_start()
        return self

    def send(self, data:Protocol):
        self.net.multi_push(data)
    
    def recv(self) -> Protocol:
        return self.net.recv_que.get()
    
    def close(self):
        self.sk.close()