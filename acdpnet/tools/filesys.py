from acdpnet.networks import endpoint as endp
from acdpnet.protocol import Protocol
from rich.console import Console
import json, os

console = Console()

print = console.print
input = console.input


class Server(endp.SocketPiont):
    def start(self):
        print(self.func)
        self.setnet('0.0.0.0', 3366)
        self.run()

    def on_list(self, meta:Protocol):
        resp = Protocol(extension='.list_resp')
        try:
            data = {
                'resp': True,
                'data': os.listdir(meta.json.get('path'))
            }
        except:
            data = {
                'resp': False
            }
        resp.upmeta(data)
        print('resping', resp.json)
        return resp


class Remote(endp.SocketTerminal):
    def listdir(self, path:str) -> list:
        data = Protocol(extension='.list')
        data.upmeta({
            'path' : path
        })
        self.send(data)
        resp = self.recv()
        print(resp.json)