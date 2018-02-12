import sys
import thread
import Tkinter as tk
import myNotebook as nb
from config import config

from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
   """Serve the client-side application."""
   #return render_template('/home/muldy/Desktop/EDMarketConnector/MissionReport/chat/index.html')
   return "hello!" 


def flaskThread():
    app.run()

def plugin_start():
   """
   Load this plugin into EDMC
   """
   thread.start_new_thread(flaskThread,())
   print "MissionReport Loaded"
   return "Mission Report"

def plugin_stop():
    """
    EDMC is closing
    """
    print "MissionReport unloaded!"



def plugin_prefs(parent, cmdr, is_beta):
   """
   Return a TK Frame for adding to the EDMC settings dialog.
   """
   this.mysetting = tk.IntVar(value=config.getint("MyPluginSetting"))	# Retrieve saved value from config
   frame = nb.Frame(parent)
   nb.Label(frame, text="Hello").grid()
   nb.Label(frame, text="Commander").grid()
   nb.Checkbutton(frame, text="My Setting", variable=this.mysetting).grid()

   return frame
