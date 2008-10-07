from xml.dom import Node
from tree_iface import TreeIface

class DomTreeIface(TreeIface):
    def __init__(self, tree):
        self._dom = tree
        self._pedigree = {}
        self._update_descendant_count(self._dom.documentElement)
    def _update_descendant_count(self, node):
        count = 1
        for n in self.get_children(node):
            count += self._update_descendant_count(n)
        node.setUserData('descendant_count', count -1, None)
        return count
    def mark_mapped(self, node):
        node.setUserData('mapped', True, None)
    def is_mapped(self, node):
        return bool(node.getUserData('mapped'))
    def mark_ordered(self, node, ordered):
#        print 'mark ordered', self.node_repr(node), ordered
        node.setUserData('ordered', ordered, None)
    def is_ordered(self, node):
#        print 'is ordered', self.node_repr(node), \
#            bool(node.getUserData('ordered'))
        return bool(node.getUserData('ordered'))
    def get_descendant_count(self, node):
        return node.getUserData('descendant_count')
    def get_children(self, node):
        if node.nodeType == node.ATTRIBUTE_NODE:
            return []
        else:
            return node.childNodes + self._attrList(node)
    def _attrList(self, node):
        if not node.attributes:
            return []
        else:
            return node.attributes.values()
    def get_parent(self, node):
        if node.nodeType == node.ATTRIBUTE_NODE:
            rv = node.ownerElement
        elif id(node) == id(self._dom.documentElement):
            return None
        else:
            rv = node.parentNode
        return rv
    def get_label(self, node):
        return '%s~%s' % (node.nodeType, node.nodeName)
    def get_value(self, node):
        try:
            return node.nodeValue
        except AttributeError:
            return getattr(node, 'data', '')
    def get_root(self):
        return self._dom.documentElement
    def deep_copy(self):
        return DomTreeIface(self._dom.cloneNode(True))
    def node_repr(self, node):
        p = node
        path = []
        while p:
            lname = self.get_label(p).split('~',1)[-1]
            if p.nodeType == Node.ATTRIBUTE_NODE:
                lname = '@' + lname
            elif p.nodeType == Node.TEXT_NODE:
                lname = 'text()'
            else:
                lname += '[%s]' % (self.get_index_in_parent(p, True) + 1)
            path.insert(0, lname)
            p = self.get_parent(p)
        return '/'+'/'.join(path)
    def move(self, node, parent, index):
        index -= 1
        if node.nodeType == node.ATTRIBUTE_NODE:
            node.ownerElement.removeAttributeNode(node)
            self._update_descendant_count(node.ownerElement)
            # Hackish, and dangerous since the node is unlinked.
            node.ownerElement = None
            parent.setAttributeNode(node)
        else:
            try:
                refnode = parent.childNodes[index]
            except IndexError:
                node.parentNode.removeChild(node)
                parent.appendChild(node)
            else:
                node.parentNode.removeChild(node)
                parent.insertBefore(node, refnode)
            self._update_descendant_count(self.get_parent(node))
        self._update_descendant_count(parent)
    def insert(self, label, value, parent, index):
        index -= 1
        node_type = int(label[:1])
        label = label.split('~', 1)[1]
        if node_type == Node.ATTRIBUTE_NODE:
            n = self._dom.createAttribute(label)
            n.value = value
        elif node_type == Node.ELEMENT_NODE:
            n = self._dom.createElement(label)
        elif node_type == Node.TEXT_NODE:
            n = self._dom.createTextNode(value)
        elif node_type == Node.COMMENT_NODE:
            n = self._dom.createComment(value)
        else:
            #TODO: More node types
            n = None
        
        if node_type == Node.ATTRIBUTE_NODE:
            parent.setAttributeNode(n)
        else:
            try:
                refnode = parent.childNodes[index]
            except IndexError:
                parent.appendChild(n)
            else:
                parent.insertBefore(n, refnode)
        self._update_descendant_count(parent)
        return n

    def delete(self, node):
        if node.nodeType == node.ATTRIBUTE_NODE:
            parent = node.ownerElement
            parent.removeAttributeNode(node)
        else:
            parent = node.parentNode
            parent.removeChild(node)
            node.unlink()
        self._update_descendant_count(parent)

    def update(self, node, val):
        if node.nodeType == node.ATTRIBUTE_NODE:
            node.ownerElement.setAttribute(node.name, val)
        if node.nodeType  in (node.TEXT_NODE, node.COMMENT_NODE):
            node.data = val

    def get_doc(self):
        return self._dom

def strip_whitespace(element):
    if element is None: 
        return
    sibling = element.firstChild
    while sibling:
        nextSibling = sibling.nextSibling
        if sibling.nodeType == Node.TEXT_NODE and sibling.data.strip() == '':
            element.removeChild(sibling)
        else:
            strip_whitespace(sibling)
        sibling = nextSibling
    

if __name__ == '__main__':
    from sys import argv
    from xml.dom.minidom import parse
    from dom_tree_matcher import DomTreeMatcher, DomVisualTreeMatcher
    from dom_tree_script import MarkChangesScriptStore
    from visualizer import VisualTreeMatcher
    from script_store import ScriptStore

    fn = ['tests/simple_tree1.xml', 'tests/simple_tree2.xml']
    if len(argv[1:]) == 2:
        fn = argv[1:]

    dom1 = parse(fn[0])
    dom2 = parse(fn[1])

    strip_whitespace(dom1)
    strip_whitespace(dom2)

    tm = DomVisualTreeMatcher(dom1, dom2, 
                        script_store=MarkChangesScriptStore)
#    tm._match()
#    tm.draw_trees(True, '/tmp/t.dot')
#    tm.print_mapping()
    s = tm.get_opcodes()
#    for i in s: print i
#    print s.get_sidebyside().toprettyxml('  ').encode('utf-8')
#    print 'inserted', s._inserted
#    print 'deleted', s._deleted
#    print 'moved', s._moved
