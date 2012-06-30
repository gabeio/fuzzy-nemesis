# really can be what ever you want as long as it servers up mako template
from gevent import monkey; monkey.patch_all()
import os, sys, bottle, gevent, json
from bottle import *
from gevent import *
from gevent.pywsgi import WSGIServer
from geventwebsocket import *
from mako.lookup import TemplateLookup

lookup = TemplateLookup(['./dynamic'])

@route('/')
def index(): yield lookup.get_template("index.mako").render()

@route('/restart/<u>/<p>') # for updates allow restart
def restart(u=None,p=None):
    if u=="DJJaxe" and p=="razr13":
        try:
            os.system("./fuzzy-nemesis") # this will run file again
            sys.exit() # this will exit this script allowing the other file to take over.
        except Exception:
            yield "server fault. did not shutdown."

@route('/static/<file:path>')
def static(file=None):
    return static_file(file, root="./")

@route('/managers')
@route('/Managers')
@route('/Managers/<pass_>')
def managers(pass_):
    if pass_ in ['Doug1','Steve2','Susan3','Gabe4']: # example passwords
        yield lookup.get_template("chat.mako").render(nick="Managers")
    else:
        yield lookup.get_template("login.mako").render() # if password is not supplied serve login

@route('/<nickname>')
def chat(nickname=None):
    yield lookup.get_template("chat.mako").render(nick=nickname)

run(host='0.0.0.0', port=10900, server='gevent')