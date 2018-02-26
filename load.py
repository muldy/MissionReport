import sys
import thread
from threading import Lock
import os
import Tkinter as tk
import myNotebook as nb
from config import config
from flask import Flask, render_template, session, request, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
import json

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__,static_url_path='/static')
#app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)#, message_queue='redis://')
flask_thread= None

this = sys.modules[__name__]	# For holding module globals
this.server_local=1
this.server_address="0.0.0.0"
this.server_port=8666



@app.route('/')
def index():
	"""Serve the client-side application."""
	return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('connect', namespace='/main')
def test_connect():
    socketio.emit('status', {'data': 'Connected'})
	print('Client connected')


@socketio.on('disconnect', namespace='/main')
def test_disconnect():
	print('Client disconnected')

def flaskThread():
    socketio.run(app,host=this.server_address,port=this.server_port)



def plugin_start():
	"""
	Load this plugin into EDMC
	"""
	flask_thread=thread.start_new_thread(flaskThread,())
	print "MissionReport Loaded"
	return "Mission Report"

def plugin_stop():
	"""
	EDMC is closing
	"""
    if flask_thread is not None:
        flask_thread.stop()
	print "MissionReport unloaded!"

def journal_entry(cmdr, is_beta, system, station, entry, state):
    socketio.emit("journal",{'data': entry},namespace='/main') 

def cmdr_data(data, is_beta):
    socketio.emit("cmdr",{'data': data},namespace='/main') 



#def plugin_prefs(parent, cmdr, is_beta):
#    """
#    Return a TK Frame for adding to the EDMC settings dialog.
#    """
#    PADX = 10
#    BUTTONX = 12	# indent Checkbuttons and Radiobuttons
#    PADY = 2		# close spacing
#
#    frame = nb.Frame(parent)
#    frame.columnconfigure(1, weight=1)
#
#    this.server_local= tk.IntVar(value=config.getint("MR_server_local"))	# Retrieve saved value from config
#    this.server_local_button=nb.Checkbutton(frame, text="Run local (127.0.0.1)", variable=,this.server_local).grid()
#    this.server_local_button.grid(columnspan=2, padx=BUTTONX, pady=(5,0), sticky=tk.W)
#
#    nb.Label(frame, text="Port").grid()
#    nb.Entry(frame, text="port").grid()
#    this.server_port= tk.IntVar(value=config.getint("MR_server_port"))	# Retrieve saved value from config
#
#    return frame

#def prefs_changed(cmdr, is_beta):
#	"""
#	Save settings.
#	"""
#    #config.set('MyPluginSetting', this.mysetting.getint())	# Store new value in config
#    pass
