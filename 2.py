from acdpnet.protocol import *
from acdpnet.tools.filesys import *

a = Remote()

a.connect('127.0.0.1', 3366)

# print(a.listdir('./'))

print(a.readfile('./1.py'))

a.close()