from subtree import *

class XmlAccessibleTree(XmlSubTree):
    def __init__(self, accessible_tree):
        XmlSubTree.__init__(self)
        self.accessibleSubtree = accessible_tree
        self.appendChild(
            self.createElementNS('http://monotonous.org/ariatest', 'ariatest'))
        self._appendNode(accessible_tree, self.documentElement)
        
    def _appendNode(self, acc, node):
        n = self.createElement('accessible')
        n.setAttribute('role', acc.accRoleName() or '')
        n.setAttribute('name', acc.accName(0) or '')

        try:
            n.setAttribute('value', acc.accValue(0) or '')
        except:
            pass

        try: 
            n.setAttribute('description', 
                                         (acc.accDescription(0) or '').strip('\x00'))
        except:
            pass
        n.setAttribute('state', '|'.join(acc.accStateSet()))
        node.appendChild(n)
        for child in acc:
          self._appendNode(child, n)

