from tree_matcher import TreeMatcher
from visualizer import VisualTreeMatcher
from script_store import ScriptStore
from dom_tree_iface import DomTreeIface
from xml.dom import Node

class DomTreeMatcher(TreeMatcher):
    def __init__(self, tree1, tree2, f=0.6, t=0.5, 
                 tree_parser=DomTreeIface, script_store=ScriptStore):
        TreeMatcher.__init__(
            self, tree1, tree2, f, t, tree_parser, script_store)
    def _match(self):
        unmatched1, unmatched2 = TreeMatcher._match(self)
        # Unravel some ill-matched attributes
        rewired = []
        for pair in self._mapping[:]:
            n1, n2 = pair
            if n1.nodeType == Node.ATTRIBUTE_NODE:
                ppartner = self._get_partner_in_t2(self._tree1.get_parent(n1))
                if ppartner != self._tree2.get_parent(n2):
                    self._mapping.remove(pair)
                    unmatched1.append(n1)
                    unmatched2.append(n2)
        for n1, n2 in [(x,y) for x in unmatched1 for y in unmatched2]:
            if (n1.nodeType, n2.nodeType) == (Node.ATTRIBUTE_NODE,)*2 and \
                    self._tree1.get_label(n1) == self._tree2.get_label(n2):
                    ppartner = self._get_partner_in_t2(self._tree1.get_parent(n1))
                    if ppartner == self._tree2.get_parent(n2):
                        self._map(n1, n2)

#    def _leaf_equal(self, node1, node2):
#        if node1.nodeType == Node.ATTRIBUTE_NODE:
#            return False # We deal with these later.
#        return TreeMatcher._leaf_equal(self, node1, node2)

class DomVisualTreeMatcher(DomTreeMatcher, VisualTreeMatcher):
    pass
