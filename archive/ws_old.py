from gevent import monkey; monkey.patch_all();
from bottle import *
from bottle.ext.websocket import *
from gevent.pywsgi import WSGIServer
from geventwebsocket import *
import json

queue=[] #saves last X amount of messages
users=[] # user list for global message

@get('/ws', apply=[websocket])
def echo(ws):
    global users, queue
    users+=[ws]
    for q in queue:
        if q is not None:
            ws.send(q)
    while True:
        msg = ws.receive()
        queue+=[msg]
        if len(queue)>10: # if messages beyond X pop X-1
            queue.pop(0)
        if msg is not None: # check to make sure message is not blank
            # note that with users possibly removed during the for loop it needs to run off the length of users not users itself.
            a=len(users) # gets users length 
            for u in range(a):
                try:
                    users[u].send(msg)
                except WebSocketError: # if users disconnected
                    users.remove(users[u-1]) # remove users
        else: break
    users.remove(ws) # supposedly remove user after disconnect

run(host='0.0.0.0', port=1025, server=GeventWebSocketServer) # start server