import Tkinter as tk
import myNotebook as nb
from config import config

this = sys.modules[__name__]	# For holding module globals


def plugin_start():
   """
   Load this plugin into EDMC
   """
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
