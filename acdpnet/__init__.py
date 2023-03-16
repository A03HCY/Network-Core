from acdpnet import protocol # base
from acdpnet import transfer # data transfer (Do not use it)
from acdpnet import networks # applications
from acdpnet import datasets # global datas
from acdpnet import tools    # tools

__version__ = '2.3.2-beta'

datasets.init()

datasets.setlist([
    'writeio', 'readio'
])
