from acdpnet.networks import endpoint
from acdpnet.protocol import Protocol 

app = endpoint.SocketPiont()

@app.route('unknow')
def uk(data):
    print(data)
    return Protocol(meta=b'fs')

app.setnet('0.0.0.0', 4440).run()