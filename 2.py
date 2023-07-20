from acdpnet.protocol import *
from acdpnet.tools.filesys import *

a = Remote()

a.connect('127.0.0.1', 3366)

# print(a.filesize('./1.py'))
# print(a.readfile('./acdpnet/protocol.py'))

print(a.listdir('./'))

print('All done')
a.close()