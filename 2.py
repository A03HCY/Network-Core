from acdpnet.protocol import *
from acdpnet.tools.filesys import *

a = Remote()

a.connect('127.0.0.1', 3366)

s = a.listdir('./')

print(s)

a.close()