from xml.dom import Node
from xml.dom.minidom import getDOMImplementation
from script_store import ScriptStore
from random import random

class MarkChangesScriptStore(ScriptStore):
    def __init__(self, tree):
        ScriptStore.__init__(self, tree)
        self._orig_tree = tree.deep_copy()
        self._pairs = dict(zip(tree.nodes_breadth(), 
                               self._orig_tree.nodes_breadth()))
        self._deleted = []
        self._inserted = []
        self._moved = []
        self._updated = []

    def move(self, node, parent, index):
        self._moved.append(
            (self._pairs[node], node, hex(abs(hash(random())))))
        ScriptStore.move(self, node, parent, index)

    def update(self, node, value):
        self._updated.append(node)
        ScriptStore.update(self, node, value)

    def insert(self, node, label, value, parent, index):
        self._inserted.append(node)
        ScriptStore.insert(self, node, label, value, parent, index)

    def delete(self, node):
        self._deleted.append(self._pairs[node])
        ScriptStore.delete(self, node)
    

    def _mark_change(self, node, change_text):
        ops = node.getAttribute('revtree:changes')
        ops = ','.join(set(filter(lambda x: bool(x), ops.split(',')) + [change_text]))
        node.setAttribute('revtree:changes', ops)

    def _add_attrib_name(self, node, key, attrib_name):
        l = node.getAttribute('revtree:'+key)
        l = ','.join(filter(lambda x: bool(x), l.split(',')) + [attrib_name])
        node.setAttribute('revtree:'+key, l)

    def get_tree_revs(self):
        tree1 = self._orig_tree
        tree2 = self._tree.deep_copy()
        pairs2 = dict(zip(self._tree.nodes_breadth(), tree2.nodes_breadth()))

        for tree in (tree1, tree2):
            tree.get_root().setAttribute(
                'xmlns:revtree', 'http://monotonous.org')
        # Move
        for n1, n2, move_id in self._moved:
            if n1.nodeType == Node.ATTRIBUTE_NODE:
                # This is complicated, just do del/ins.
                self._deleted.append(n1)
                self._inserted.append(n2)
            elif n1.nodeType == Node.TEXT_NODE:
                self._mark_change(n1.parentNode, 'moved-text')
                n1.parentNode.setAttribute(
                    'revtree:moveTextId', move_id+'Left')
                self._mark_change(pairs2[n2.parentNode], 'moved-text')
                pairs2[n2.parentNode].setAttribute(
                    'revtree:moveTextId', move_id+'Right')
            else:
                self._mark_change(n1, 'moved-self')
                n1.setAttribute('revtree:moveId', move_id+'Left')
                self._mark_change(pairs2[n2], 'moved-self')
                pairs2[n2].setAttribute('revtree:moveId', move_id+'Right')

        # Delete
        for n in self._deleted:
            if n.nodeType == Node.TEXT_NODE:
                if n.parentNode not in self._deleted:
                    self._mark_change(n.parentNode, 'deleted-text')
            elif n.nodeType == Node.ATTRIBUTE_NODE:
                if n.ownerElement not in self._deleted:
                    self._mark_change(n.ownerElement, 'deleted-attrib')
                    self._add_attrib_name(
                        n.ownerElement, 'deletedAttribs', n.name)
            else:
                self._mark_change(n, 'deleted-self')

        # Insert
        for n in self._inserted:
            #n = pairs2[n]
            if n.nodeType == Node.TEXT_NODE:
                if n.parentNode not in self._inserted:
                    self._mark_change(pairs2[n.parentNode], 'inserted-text')
            elif n.nodeType == Node.ATTRIBUTE_NODE:
                if n.ownerElement not in self._inserted:
                    self._mark_change(pairs2[n.ownerElement], 
                                      'inserted-attrib')
                    self._add_attrib_name(
                        pairs2[n.ownerElement], 'insertedAttribs', n.name)
            else:
                self._mark_change(pairs2[n], 'inserted-self')

        # Update
        for n in self._updated:
            if n.nodeType == Node.ATTRIBUTE_NODE:
                self._mark_change(pairs2[n.ownerElement], 
                                      'updated-attrib')
                self._add_attrib_name(
                        pairs2[n.ownerElement], 'updatedAttribs', n.name)
            elif n.nodeType == Node.TEXT_NODE:
                self._mark_change(pairs2[n].parentNode, 'updated-text')
        
        return tree1.get_doc(), tree2.get_doc()

    def get_sidebyside(self):
        doc = getDOMImplementation().createDocument('', 'sidebyside', None)
        doc1, doc2 = self.get_tree_revs()
        left = doc.createElement('left')
        left.appendChild(doc1.documentElement)
        doc.documentElement.appendChild(left)
        right = doc.createElement('right')
        right.appendChild(doc2.documentElement)
        doc.documentElement.appendChild(right)
        return doc
        

class XupdateScriptStore(ScriptStore):
    def __init__(self, tree):
        self._tree = tree
        self._xupdate_doc = getDOMImplementation().createDocument(
            'http://www.xmldb.org/xupdate', 'xupdate:modifications', None)
        self._inserted_ancestor = None
        list.__init__(self)

    def append(self, val):
        list.append(self, val)

    def _append_instruction(self, instruction, select):
        element = self._xupdate_doc.createElement('xupdate:' + instruction)
        element.setAttribute('select', select)
        self._xupdate_doc.documentElement.appendChild(element)
        return element

    def _append_comment(self, comment):
        c = self._xupdate_doc.createComment(comment)
        self._xupdate_doc.documentElement.appendChild(c)
        return c

    def _flush_inserts(self):
        if self._inserted_ancestor:
            self._append_comment('Insert')
            sibling = self._inserted_ancestor.previousSibling
            if sibling:
                element = self._append_instruction(
                    'insert-after', 
                    self._tree.node_repr(sibling))
            else:
                element = self._append_instruction(
                    'append', 
                    self._tree.node_repr(
                        self._tree.get_parent(self._inserted_ancestor) or '/'))
            if self._inserted_ancestor.nodeType == \
                    self._inserted_ancestor.ATTRIBUTE_NODE:
                element.setAttributeNode(
                    self._inserted_ancestor.cloneNode(True))
            else:
                element.appendChild(self._inserted_ancestor.cloneNode(True))
            self._inserted_ancestor = None

    def _is_ancestor(self, node, ancestor):
        parent = self._tree.get_parent(node)
        while parent:
            if parent == ancestor:
                return True
            parent = self._tree.get_parent(parent)
        return False
            

    def move(self, node, parent, index):
        self._flush_inserts()

        self._append_comment('Move')

        element = self._append_instruction('variable', 
                                           self._tree.node_repr(node))
        element.setAttribute('name', node.nodeName.split(':')[-1])

        self._append_instruction('remove', 
                                           self._tree.node_repr(node))

        try:
            sibling = parent.childNodes[index + 1]
        except IndexError:
            element = self._append_instruction('append', 
                                     self._tree.node_repr(parent))
        else:
            element = self._append_instruction('insert-before', 
                                     self._tree.node_repr(sibling))

        val_of = self._xupdate_doc.createElement('xupdate:value-of')
        val_of.setAttribute('select', '$' + node.nodeName.split(':')[-1])
        element.appendChild(val_of)

            
        self.append(
            'MOV(%s, %s, %s)' % \
                (self._tree.node_repr(node), 
                 self._tree.node_repr(parent), index))



    def insert(self, node, label, value, parent, index):
        if not self._inserted_ancestor:
            self._inserted_ancestor = node
        elif not self._is_ancestor(node, self._inserted_ancestor):
            self._flush_inserts()

        self.append(
            'INS((%s, %s, %s), %s, %s)' % \
                (self._tree.node_repr(node), label, value, 
                 self._tree.node_repr(parent), index))

    def update(self, node, value):
        self._flush_inserts()
        self._append_comment('Update')
        element = self._append_instruction('update', self._tree.node_repr(node))

        self._flush_inserts()

        self.append('UPD(%s, %s)' % (self._tree.node_repr(node), value))

    def delete(self, node):
        self._flush_inserts()
        self._append_comment('Delete')
        element = self._append_instruction('remove', self._tree.node_repr(node))

        self.append('DEL(%s)' % self._tree.node_repr(node))

class SideBySideScript(ScriptStore):
    def __init__(self, tree):
        self._orig_tree = tree.deep_copy()
        ScriptStore.__init__(self, tree)

    def get_trees(self):
        doc = getDOMImplementation().createDocument('', 'sidebyside', None)
        left = doc.createElement('left')
        left.appendChild(self._orig_tree.get_root())
        doc.documentElement.appendChild(left)
        right = doc.createElement('right')
        right.appendChild(self._tree.get_root())
        doc.documentElement.appendChild(right)
        return doc

    def _append_comment(self, doc, comment):
        c = doc.createComment(comment)
        doc.documentElement.appendChild(c)
        return c

    def _path_template(self, doc, xpath, attribs={}):
        template = doc.createElement('xsl:template')
        template.setAttribute('match', xpath)
        copy = doc.createElement('xsl:copy')
        copy.setAttribute('select', '@*')
        template.appendChild(copy)
        for key, value in attribs.items():
            a = doc.createElement('xsl:attribute')
            a.setAttribute('name', key)
            copy.appendChild(a)
            a.appendChild(doc.createTextNode(value))
        copy.appendChild(doc.createElement('xsl:apply-templates'))
        return template

    def _node_type_from_xpath(self, xpath):
        n_str = xpath.split('/')[-1]
        if n_str.startswith('@'):
            return Node.ATTRIBUTE_NODE
        elif n_str == 'text()':
            return Node.TEXT_NODE
        else:
            return Node.ELEMENT_NODE 

    def get_xsl(self):
        doc = getDOMImplementation().createDocument(
            'http://www.w3.org/1999/XSL/Transform', 'xsl:stylesheet', None)
        # BUG: The namespace thingy doesn't work.
        doc.documentElement.setAttribute(
            'xmlns:xsl', 'http://www.w3.org/1999/XSL/Transform')
        for op in self:
            if op.op_type == op.DELETE:
                del_path = op.args[0]
                if self._node_type_from_xpath(del_path) == Node.ELEMENT_NODE:
                    self._append_comment(doc, 'Delete Element')
                    template = self._path_template(
                        doc, 'left' +del_path, {'revised' : 'deleted'})
                    doc.documentElement.appendChild(template)
                elif self._node_type_from_xpath(del_path) == Node.TEXT_NODE:
                    self._append_comment(doc, 'Delete Text')
                    del_path = del_path[:del_path.rindex('/')]
                    template = self._path_template(
                        doc, 'left' +del_path, {'revised' : 'deleted-text'})
                    doc.documentElement.appendChild(template)
                    
        self._append_comment(doc, 'Generic')
        template = self._path_template(doc, '*')
        doc.documentElement.appendChild(template)
        return doc
            

if __name__ == '__main__':
    from sys import argv
    fn = ['tests/simple_tree1.xml', 'tests/simple_tree2.xml']
    if len(argv[1:]) == 2:
        fn = argv[1:]

    from xml.dom.minidom import parse
    from dom_tree_matcher import DomTreeMatcher
    dom1 = parse(fn[0])
    dom2 = parse(fn[1])
    tm = DomTreeMatcher(dom1, dom2, script_store=SideBySideScript)
    
    s = tm.get_opcodes()
    a = open('/tmp/t.xsl', 'w')
    xsl = s.get_xsl()
    xsl.writexml(a)
    a.close()

    a = open('/tmp/t.xml', 'w')
    s.get_trees().writexml(a, ' ',' ', '\n')
    a.close()
    

