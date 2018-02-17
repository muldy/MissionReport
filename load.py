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
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)#, message_queue='redis://')
#socketio_c = SocketIO(message_queue='redis://')
thready = None
flask_thread= None
thread_lock = Lock()

this = sys.modules[__name__]	# For holding module globals
this.server_local=1
this.server_address="0.0.0.0"
this.server_port=8666



@app.route('/')
def index():
	"""Serve the client-side application."""
	return render_template('index.html', async_mode=socketio.async_mode)

def background_thread():
	"""Example of how to send server generated events to clients."""
	count = 0
	while True:
		socketio.sleep(10)
		count += 1
		socketio.emit('my_response',
			{'data': 'Server generated event', 'count': count},
			namespace='/test')

@socketio.on('my_event', namespace='/test')
def test_message(message):
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_response',
		{'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_response',
		{'data': message['data'], 'count': session['receive_count']},
		broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
	join_room(message['room'])
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_response',
		{'data': 'In rooms: ' + ', '.join(rooms()),
		'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
	leave_room(message['room'])
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_response',
		{'data': 'In rooms: ' + ', '.join(rooms()),
		'count': session['receive_count']})


@socketio.on('close_room', namespace='/test')
def close(message):
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
	'count': session['receive_count']},
	room=message['room'])
	close_room(message['room'])


@socketio.on('my_room_event', namespace='/test')
def send_room_message(message):
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_response',
		{'data': message['data'], 'count': session['receive_count']},
		room=message['room'])


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_response',
		{'data': 'Disconnected!', 'count': session['receive_count']})
	disconnect()


@socketio.on('my_ping', namespace='/test')
def ping_pong():
	emit('my_pong')


@socketio.on('connect', namespace='/test')
def test_connect():
	#global thready
	#with thread_lock:
	#	if thready is None:
	#		thready = socketio.start_background_task(target=background_thread)
	#emit('my_response', {'data': 'Connected', 'count': 0})
        socketio.emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
	print('Client disconnected', request.sid)

def flaskThread():
    #app.run(host='0.0.0.0.',port=8666)
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
	with thread_lock:
		if thready is not None:
			print "stop threads"
			thready.stop()
			flask_thread.stop()
	print "MissionReport unloaded!"

def journal_entry(cmdr, is_beta, system, station, entry, state):
    print "RESPONSE: **********************" 
    print str(entry)
    print "RESPONSE: **********************" 
    #socketio_c.emit("my_response",json.loads(entry))
    socketio.emit("my_response",{'data': entry, 'count': 0},namespace='/test') 

def cmdr_data(data, is_beta):
    print "RESPONSE: **********************"
    print str(data) 
    print "RESPONSE: **********************"
    #socketio_c.emit("my_response",json.loads(data)) 
    socketio.emit("my_response",{'data': data, 'count': 0},namespace='/test') 



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
