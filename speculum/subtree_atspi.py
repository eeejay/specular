from subtree import *

class XmlAccessibleTree(XmlSubTree):
    def __init__(self, accessible_tree):
        XmlSubTree.__init__(self)
        self.accessibleSubtree = accessible_tree
        self._appendNode(accessible_tree, self)
        
    def _appendNode(self, acc, node):
        n = self.createElement('accessible')
        n.setAttribute('role', acc.getRoleName())
        n.setAttribute('name', acc.name)

        n.setAttribute('description', acc.description)
        
        sset = [repr(a)[6:].lower() for a in acc.getState().getStates()]
        
        n.setAttribute('state', '|'.join(sset))
        node.appendChild(n)
        for child in acc:
            if child is None: continue
            self._appendNode(child, n)

