from gevent import monkey; monkey.patch_all();
from bottle import *
from bottle.ext.websocket import *
from gevent.pywsgi import WSGIServer
from geventwebsocket import *
import json

install(websocket)

managers=[]
queue=[] # saves last X amount of messages
users={} # user list for global message
pwds=[] # passwords go here

# password adjustments coming in next push
# add passwords coming in next push
# typing to coming in next(2) pushes

@route('/Managers/<pwd>')
def mans(ws, pwd, *catch, **catching):
    global pwds, managers, users, queue
    if pwd in pwds:
        managers+=[ws]
        try:
            for q in queue:
                if q is not None:
                    ws.send(q)
        except Exception: pass
        while True:
            msg = ws.receive()
            try:
                to = json.loads(msg)['data']['to']
            except Exception:
                to = ""
            try:
                message = json.loads(msg)['data']['message']
            except Exception:
                message = ""
            if msg is not None:
                if message!="" and to!="":
                    queue+=[msg]
                    if len(queue)>15:
                        queue.pop(0)
                    try:
                        a=len(managers)
                        for u in range(a):
                            try:
                                managers[u].send(msg)
                            except WebSocketError:
                                managers.remove(managers[u-1])
                        users[to].send(msg)
                    except WebSocketError: # if users disconnected
                        del users[to] # remove users
            else: break
        try:
            managers.remove(managers.index(ws)) # supposedly remove user after disconnect
        except Exception: pass

@route('/<name>')
def clients(ws, name, *catch, **catching):
    global users, queue
    try:
        if users[name]:
            msg=json.dumps({"type":"message","data":{"to":name,"nick":"System","message":name+" is already in use."}})
            ws.send(msg)
    except Exception:pass
    users[name]=ws
    if len(managers) == 0:
        msg=json.dumps({"type":"message","data":{"to":name,"nick":"Managers","message":"Sorry "+name+", but there are no managers online."}})
        ws.send(msg)
        yield
        return
    msg=json.dumps({"type":"message","data":{"to":name,"nick":"Managers","message":"Hello "+name+", how can we help you today?"}})
    ws.send(msg)
    msg=json.dumps({"type":"message","data":{"to":"Managers","nick":"System","message":name+" signed in."}})
    a=len(managers)
    for u in range(a):
        try:
            managers[u].send(msg)
        except WebSocketError:
            del managers[u]
    while True:
        msg = ws.receive()
        try:
            message = json.loads(msg)['data']['message']
        except Exception:
            message = ""
        if msg!=None:
            if message!="":
                queue+=[msg]
                if len(queue)>15:
                    queue.pop(0)
                a=len(managers)
                for u in range(a):
                    try:
                        managers[u].send(msg)
                    except WebSocketError:
                        managers.remove(managers[u-1])
        else: break
    msg=json.dumps({"type":"message","data":{"to":"Managers","nick":"System","message":name+" signed out."}})
    a=len(managers)
    for u in range(a):
        try:
            managers[u].send(msg)
        except WebSocketError:
            del managers[u]
    try:
        del users[name]
    except Exception: pass

run(host='0.0.0.0', port=1025, server=GeventWebSocketServer) # start server