fuzzy-nemesis
=============

A "Chat with a manager" written in python

I actually wrote this for my job but its my code and I choose to make it open source.

The idea behind is it that all the clients can only message the Manager but the Manager can reply to all of the clients.

Features (version 2)
========
- Clients can send messages only to Managers (all of the online managers)
- Managers can send messages to anyone
- Only intended client receives messages
- All online managers receive all messages sent by other managers and messages from clients
- Manager page is password protected

Coming Soon
===========
- Managing Manager passwords (changing your password)
- Deleting Manager
- Adding Manager
- See Who Other Managers are answering
- Manager/Client Isolation (When manager clicks on clients name clients messages will be highlighted & other clients will be dimmed & other managers will see this and will be warned upon joining isolation)

Requirements
============
- Python 2.7+?
- Gevent
- Gevent-websocket
- bottle
- bottle-websocket
- makotemplates

Install
=======
Just place the files wherever you want.

Run
===
`python runme.py`