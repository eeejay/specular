from specular_serial import SpecularSerial
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
    dom = parseString(acc_str)
    return specular_accessible_from_dom(dom.documentElement)

def specular_accessible_from_file(file):
    dom = parse(file)
    return specular_accessible_from_dom(dom.documentElement)

def specular_accessible_from_dom(dom):
    return SpecularAccessible(dom)


if platform == 'win32':
    def _populate_accessible_node(doc, element, acc):
        element.setAttribute('role', acc.accRoleName() or '')
        element.setAttribute('name', acc.accName(0) or '')

        try:
            element.setAttribute('value', acc.accValue(0) or '')
        except:
            pass

        try: 
            element.setAttribute('description', 
                                 (acc.accDescription(0) or '').strip('\x00'))
        except:
            pass

        element.setAttribute('state', '|'.join(acc.accStateSet()))
        
        for child in acc:
            if child:
                e = doc.createElement('accessible')
                element.appendChild(e)
                _populate_accessible_node(doc, e, child)
else:
    def _populate_accessible_node(doc, element, acc):
        element.setAttribute('role', acc.getRoleName())
        element.setAttribute('name', acc.name)

        element.setAttribute('description', acc.description)
        
        sset = [repr(a)[6:].lower() for a in acc.getState().getStates()]
        
        element.setAttribute('state', '|'.join(sset))
        for child in acc:
            if child:
                e = doc.createElement('accessible')
                element.appendChild(e)
                _populate_accessible_node(doc, e, child)

def specular_accessible_from_accessible(acc):    
    doc = getDOMImplementation().createDocument(None, "accessible", None)
    _populate_accessible_node(doc, doc.documentElement, acc)
    return specular_accessible_from_dom(doc.documentElement)
