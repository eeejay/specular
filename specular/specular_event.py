# Specular
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
#
# The Initial Developer of the Original Code is Eitan Isaacson.
# Portions created by the Initial Developer are Copyright (C) 2008
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Original Author: Eitan Isaacson (eitan@ascender.com)
#
# Alternatively, the contents of this file may be used under the terms of
# either of the GNU General Public License Version 2 or later (the "GPL"),
# or the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.

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
