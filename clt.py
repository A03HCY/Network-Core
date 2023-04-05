from acdpnet.tools.filesys import *


class Command:
    @staticmethod
    def file(args):
        mode = input('设置模式\n> ')
        if mode == 'server':
            try:
                Server().start()
            except:pass
            print('service closed')
            return
        if mode == 'client':
            pass


class App:
    def __init__(self) -> None:
        self.real = []
        for i in dir(Command):
            if '__' in i:continue
            self.real.append(i)

    def endpiont(self):
        comd = self.input().split(' ')
        if comd[0] in self.real:
            self.exec(comd)
    
    def input(self) -> str:
        data = input('# ')
        return data
    
    def exec(self, comd:list):
        func = getattr(Command, comd[0])
        func(comd[0:])


a = App()

a.endpiont()