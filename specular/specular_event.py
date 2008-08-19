from sys import platform
from xml.dom.minidom import \
    Document, Node, parse, parseString, getDOMImplementation
from specular_serial import SpecularSerial, strip_whitespace
from specular_accessible import \
    specular_accessible_from_accessible, \
    specular_accessible_from_dom, \
    specular_accessible_from_string

if platform == 'win32':
    import pyia
    events_map = {'object-state-changed':pyia.EVENT_OBJECT_STATECHANGE}
    def get_specular_type(native_type):
        for key, value in events_map.iteritems():
            if value == native_type:
                return key
else:
    events_map = {'object-state-changed':'object:state-changed'}
    def get_specular_type(native_type):
        for key, value in events_map.iteritems():
            if native_type.startswith(value):
                return key


class SpecularEvent(SpecularSerial):
    def __init__(self, root_element):
        SpecularSerial.__init__(self, root_element)
        self.type = self.documentElement.getAttribute('type')
        source = self.getElementsByTagName('accessible')
        if source:
            self.source = specular_accessible_from_string(source[0].toxml())
        else:
            self.source = specular_accessible_from_string('<accessible/>')

    @property 
    def native_type(self):
        return events_map[self.type]

    def match(self, other):
        if other.type == self.type:
            if self.source.compareNode(other.source):
                return True
        return False
    

def specular_event_from_string(event_str):
    dom = parseString(event_str)
    strip_whitespace(dom.documentElement)
    return specular_event_from_dom(dom.documentElement)

def specular_event_from_file(file):
    dom = parse(file)
    strip_whitespace(dom.documentElement)
    return specular_event_from_dom(dom.documentElement)

def specular_event_from_dom(dom):
    return SpecularEvent(dom)

def specular_event_from_event(event):
    doc = Document()
    doc.appendChild(doc.createElement('event'))
    doc.documentElement.setAttribute('type', get_specular_type(event.type))
    if event.source:
        acc_dom = specular_accessible_from_accessible(event.source)
        source = doc.createElement('source')
        doc.documentElement.appendChild(source)
        source.appendChild(acc_dom.documentElement)
    return specular_event_from_dom(doc.documentElement)
