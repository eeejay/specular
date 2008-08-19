from sys import platform
from xml.dom.minidom import \
    Document, Node, parse, parseString, getDOMImplementation
from specular_serial import SpecularSerial
from specular_accessible import specular_accessible_from_accessible

if platform == 'win32':
    import pyia
    events_map = {'object-state-changed':pyia.EVENT_OBJECT_STATECHANGE}
else:
    events_map = {'object-state-changed':'object:state-changed'}

def get_specular_type(native_type):
    for key, value in events_map.iter_items():
        if value == native_type:
            return key

class SpecularEvent(SpecularSerial):
    def __init__(self, root_element):
        SpecularSerial.__init__(self, root_element)
        self.type = self.documentElement.getAttribute('type')
        source = edom.getElementsByTagName('accessible')
        if source:
            self.source = specular_accessible_from_dom(source[0])
        else:
            self.source = None
    @property 
    def native_type(self):
        return events_map[self.type]
    

def specular_event_from_string(event_str):
    dom = parseString(event_str)
    return specular_event_from_dom(dom.documentElement)

def specular_event_from_file(file):
    dom = parse(file)
    return specular_event_from_dom(dom.documentElement)

def specular_event_from_dom(dom):
    return specular_event_from_dom(dom.documentElement)

def specular_event_from_event(event):
    doc = getDOMImplementation().createDocument(None, "event", None)
    doc.documentElement.setAttribute('type', get_specular_type(event.type))
    if event.source:
        acc_dom = specular_accessible_from_accessible(event.source)
        source = doc.createElement('source')
        doc.documentElement.appendChild(source)
        source.appendChild(acc_dom.documentElement)
    return specular_accessible_from_dom(doc.documentElement)
