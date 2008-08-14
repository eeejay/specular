from sys import platform

EVENT_OBJECT_STATECHANGE = 0

if platform == 'win32':
    import pyia
    events_map = {EVENT_OBJECT_STATECHANGE:pyia.EVENT_OBJECT_STATECHANGE}
else:
    import pyatspi
    events_map = {EVENT_OBJECT_STATECHANGE:'object:state-changed'}

