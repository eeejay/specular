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
# The Original Code is mozilla.org code.
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

from xml.dom.minidom import Document, Node, parse, parseString
from fnmatch import translate as glob_trans
from re import match as re_match
from sys import platform

debug = False

def debug_print(s):
    if debug:
        print s

class SpecularSerial(Document):
    def __init__(self, root_element):
        Document.__init__(self)
        self.appendChild(root_element)

    def compare(self, other):
        if isinstance(other, Document):
            other = other.documentElement
        return self._compare(self.documentElement, other)

    def _compare(self, node1, node2):
        if not self._compareNode(node1, node2):
            return False
        for child1, child2 in zip(node1.childNodes, node2.childNodes):
            if not self._compare(child1, child2):
                debug_print('child compare failed')
                return False
        return True

    def compareNode(self, other):
        if isinstance(other, Document):
            other = other.documentElement
        rv = self._compareNode(self.documentElement, other)
        print rv
        return rv

    def _compareNode(self, node1, node2):
        if node1.nodeName != node2.nodeName:
            debug_print('node name mismatch')
            return False
        for attrib in node2.attributes.keys():
            if not self._compareAttribute(node1, node2, attrib):
                debug_print('attrib mismatch (%s) %s %s' % 
                            (attrib,
                             node1.getAttribute(attrib),
                             node2.getAttribute(attrib)))
                return False
        return True

    def _compareAttribute(self, node1, node2, attr):
        attr1 = node1.getAttribute(attr)
        attr2 = node2.getAttribute(attr)
        if attr2.startswith('regexp:'):
            return bool(re_match(attr2[7:], attr1))
        elif attr2.startswith('glob:'):
            return bool(re_match(glob_trans(attr2[5:]), attr1))
        else:
            return attr1 == attr2

def strip_whitespace(element):
    if element is None: 
        return
    sibling = element.firstChild
    while sibling:
        nextSibling = sibling.nextSibling
        if sibling.nodeType == Node.TEXT_NODE:
            element.removeChild(sibling)
        else:
            strip_whitespace(sibling)
        sibling = nextSibling
