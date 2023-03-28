from acdpnet.networks import endpoint
from acdpnet.protocol import Protocol 

app = endpoint.SocketTerminal()

@app.route('unknow')
def uk(data):
    print('rv', data)
    input('> ')
    app.close()
    print('close')

app.setnet('0.0.0.0', 4440).connect()

app.send(Protocol(b'ft'))
print('ok')
app.keep()