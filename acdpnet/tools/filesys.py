from acdpnet.networks import endpoint as endp
from acdpnet.protocol import Protocol
from rich.console import Console
import os

console = Console()

print = console.print
input = console.input


class ost:
    @staticmethod
    def listdir(path:str) -> list:
        info = []
        for i in os.scandir(path):
            info.append([i.name, i.is_file(), list(i.stat())])
        return info


class Server(endp.SocketPiont):
    def start(self):
        print(self.func)
        self.setnet('0.0.0.0', 3366)
        self.run()

    def on_listdir(self, meta:Protocol):
        resp = Protocol(extension='.listdir_resp')
        try:
            data = {
                'resp': True,
                'data': ost.listdir(meta.json.get('path'))
            }
        except:
            data = {
                'resp': False
            }
        resp.upmeta(data)
        print('resping', resp)
        return resp
    
    def on_readfile(self, meta:Protocol):
        resp = Protocol(extension='.readfile_resp')
        path = meta.json.get('path')
        buff = meta.json.get('buff', 0)
        seek = meta.json.get('seek', 0)
        if not os.path.isfile(path):
            data = {
                'resp': False, 
                'info': 'Not found'
            }
            resp.upmeta(data)
            return resp
        size = os.path.getsize(path)
        if seek >= size:
            data = {
                'resp': False, 
                'info': 'Seek out of range'
            }
            resp.upmeta(data)
            return resp
        size -= seek
        with open(path, 'rb') as f:
            f.seek(seek)
            if buff == 0:
                print('全发送')
                cont = f.read()
            elif buff <= size:
                print('buff 发送')
                cont = f.read(buff)
            else:
                print('size 发送')
                cont = f.read(size)
        resp.meta = cont
        resp.extn = '.readfile_meta'
        return resp
    
    def on_file(self, meta:Protocol):
        resp = Protocol(extension='.file_resp')
        path = meta.json.get('path')
        optn = meta.json.get('option')
        if not os.path.isfile(path):
            resp.upmeta({
                'resp':False
            })
            return resp
        if optn == 'size':
            resp.upmeta({
                'resp': True,
                'size': os.path.getsize(path)
            })
            return resp
    

class Remote(endp.SocketTerminal):
    def listdir(self, path:str) -> list:
        data = Protocol(extension='.listdir')
        data.upmeta({
            'path' : path
        })
        self.send(data)
        resp = self.recv()
        return resp.json.get('data', [])
    
    def readfile(self, path:str, seek:int=0, buff:int=0) -> bytes:
        data = Protocol(extension='.readfile')
        data.upmeta({
            'path': path,
            'seek': seek,
            'buff': buff
        })
        self.send(data)
        resp = self.recv()
        if '_resp' in resp.extn:
            raise IOError('')
        return resp.meta
    
    def filesize(self, path:str) -> int:
        data = Protocol(extension='.file')
        data.upmeta({
            'path': path,
            'option': 'size'
        })
        self.send(data)
        resp = self.recv()
        if resp.json.get('resp') == False:
            raise IOError()
        return resp.json.get('size')