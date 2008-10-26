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

from specular_serial import SpecularSerial, strip_whitespace
from sys import platform
from xml.dom.minidom import \
    Document, Node, parse, parseString, getDOMImplementation

class SpecularAccessible(SpecularSerial):
    def find_subtree(self, other_subtree):
        if isinstance(other_subtree, Document):
            other_subtree = other_subtree.documentElement
        return self._find_subtree(self.documentElement, other_subtree)

    def _find_subtree(self, node, other_subtree):
        if self._compare(node, other_subtree):
            return node
        for child in node.childNodes:
            n = self._find_subtree(child, other_subtree)
            if n:
                return n
        return None

def specular_accessible_from_string(acc_str):
    dom = parseString(acc_str.encode('utf-8'))
    strip_whitespace(dom.documentElement)
    return specular_accessible_from_dom(dom.documentElement)

def specular_accessible_from_file(file):
    dom = parse(file)
    strip_whitespace(dom.documentElement)
    return specular_accessible_from_dom(dom.documentElement)

def specular_accessible_from_dom(dom):
    return SpecularAccessible(dom)


if platform == 'win32':
    def _populate_accessible_node(doc, element, acc, descendants=True):
        element.setAttribute('role', unicode(acc.accRoleName() or ''))
        element.setAttribute('name', unicode(acc.accName(0) or ''))

        try:
            element.setAttribute('value', unicode(acc.accValue(0) or ''))
        except:
            pass

        try: 
            element.setAttribute('description', 
                                 unicode((acc.accDescription(0) or '').strip('\x00')))
        except:
            pass

        element.setAttribute('state', u'|'.join(acc.accStateSet()))
        
        if descendants:
            for child in acc:
                if child:
                    e = doc.createElement('accessible')
                    element.appendChild(e)
                    _populate_accessible_node(doc, e, child)
else:
    def _populate_accessible_node(doc, element, acc, descendants=True):
        element.setAttribute('role', unicode(acc.getRoleName(), 'utf-8'))
        element.setAttribute('name', unicode(acc.name, 'utf-8'))

        element.setAttribute('description', unicode(acc.description, 'utf-8'))

        val = ''
        try:
            ivalue = acc.queryValue()
        except NotImplementedError:
            try:
                itext = acc.queryText()
            except NotImplementedError:
                pass
            else:
                val = itext.getText(0,-1)
        else:
            val = str(ivalue.currentValue)

        element.setAttribute('value', unicode(val, 'utf-8'))
        
        sset = [repr(a)[6:].lower() for a in acc.getState().getStates()]
        
        element.setAttribute('state', u'|'.join(sset))
        if descendants:
            for child in acc:
                if child:
                    e = doc.createElement('accessible')
                    try:
                        _populate_accessible_node(doc, e, child)
                    except LookupError:
                        pass
                    else:
                        element.appendChild(e)

def specular_accessible_from_accessible(acc, descendants=True):    
    if not acc: return None
    doc = getDOMImplementation().createDocument(None, "accessible", None)
    _populate_accessible_node(doc, doc.documentElement, acc, descendants)
    return specular_accessible_from_dom(doc.documentElement)
