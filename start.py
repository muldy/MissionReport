def plugin_start():
   """
   Load this plugin into EDMC
   """
   print "MissionReport Loaded"
   return "All done"

def plugin_stop():
    """
    EDMC is closing
    """
    print "MissionReport unloaded!"
