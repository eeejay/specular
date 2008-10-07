class TreeIface:
    def __init__(self, tree):
        pass
    def mark_mapped(self, node):
        raise NotImplemented
    def is_mapped(self, node):
        raise NotImplemented
    def mark_ordered(self, node, ordered):
        raise NotImplemented
    def mark_children_unordered(self, node):
        for child in self.get_children(node):
            self.mark_ordered(child, False)
    def is_ordered(self, node):
        raise NotImplemented
    def get_descendant_count(self, node):
        raise NotImplemented
    def get_children(self, node):
        raise NotImplemented
    def get_parent(self, node):
        raise NotImplemented
    def get_label(self, node):
        raise NotImplemented
    def get_value(self, node):
        raise NotImplemented
    def get_root(self):
        raise NotImplemented
    def cache_pedigree(self, node):
        pedigree = []
        p = self.get_parent(node)
        while p:
            pedigree.append(id(p))
            p = self.get_parent(p)
        self._pedigree[id(node)] = pedigree
    def is_descendant(self, node, ancestor):
        pedigree = self._pedigree.get(id(node), [])
        return id(ancestor) in pedigree
    def get_index_in_parent(self, node, with_same_label=False):
        parent = self.get_parent(node)
        if not parent:
            return 0
        if with_same_label:
            nlabel = self.get_label(node)
            children = filter(lambda x: self.get_label(x) == nlabel,
                             self.get_children(parent))
        else:
            children = self.get_children(parent)
        return children.index(node)
    def deep_copy(self):
        raise NotImplemented
    def node_repr(self, node):
        raise NotImplemented
    def move(self, node, parent, index):
        raise NotImplemented
    def insert(self, label, value, parent, insert):
        raise NotImplemented
    def delete(self, node):
        raise NotImplemented
    def update(self, node, val):
        raise NotImplemented
    def nodes_breadth(self):
        def _nodes_breadth(node, l):
            for n in self.get_children(node):
                l.append(n)
            for n in self.get_children(node):
                _nodes_breadth(n, l)
            return l
        return _nodes_breadth(self.get_root(), [self.get_root()])
    def nodes_postorder(self):
        def _nodes_postorder(node, l):
            for n in self.get_children(node):
                _nodes_postorder(n, l)
            l.append(node)
            return l
        return _nodes_postorder(self.get_root(), [])
    def print_tree(self):
        def _print_tree(node, indent=0):
            print '%s%s %s' % (' '*indent, self.node_repr(node), 
                               self.node_repr(self.get_parent(node)))
            for n in self.get_children(node):
                _print_tree(n, indent+1)
        _print_tree(self.get_root())
    def get_labels(self):
        def _get_labels(node, middle_labels, leaf_labels):
            if node and self.get_children(node):
                for n in self.get_children(node):
                    _get_labels(n, middle_labels, leaf_labels)
                if node != self.get_root():
                    middle_labels.setdefault(
                        self.get_label(node), []).append(node)
            elif node:
                leaf_labels.setdefault(
                    self.get_label(node), []).append(node)
        leaf_labels = {}
        middle_labels = {}
        _get_labels(self.get_root(), middle_labels, leaf_labels)
        return leaf_labels, middle_labels
        
class ListTreeIface(TreeIface):
    LABEL = 0
    VALUE = 1
    CHILDREN = 2
    def __init__(self, tree):
        self._tree = tree
        self._mapped = set()
        self._ordered = set()
        self._pedigree = {}
        self._parents = {}
        self._descendant_count = {}
        self._double_link(self._tree)
    def _double_link(self, node):
        count = 1
        for n in node[self.CHILDREN]:
            self._parents[id(n)] = node
            count += self._double_link(n)
        self._descendant_count[id(node)] = count - 1
        return count
    def mark_mapped(self, node):
        self._mapped.add(id(node))
    def is_mapped(self, node):
        return id(node) in self._mapped
    def mark_ordered(self, node, ordered):
        if ordered:
            self._ordered.add(id(node))
        else:
            try:
                self._ordered.remove(id(node))
            except KeyError:
                pass
    def is_ordered(self, node):
        return id(node) in self._ordered
    def get_descendant_count(self, node):
        return self._descendant_count[id(node)]
    def get_children(self, node):
        return node[self.CHILDREN]
    def get_parent(self, node):
        return self._parents.get(id(node), None)
    def get_label(self, node):
        return node[self.LABEL]
    def get_value(self, node):
        return node[self.VALUE]
    def get_root(self):
        return self._tree
    def node_repr(self, node):
        if node is None: return None
        s = '%s:%s' % (self.get_label(node), self.get_value(node))
        while self.get_parent(node):
            child = node
            node = self.get_parent(node)
            s = '%s:%s[%s]/%s' % \
                (self.get_label(node), self.get_value(node) or '', 
                 self.get_index_in_parent(child), s)
        return s
    def move(self, node, parent, index):
        old_parent = self.get_parent(node)
        if old_parent:
            old_parent[self.CHILDREN].remove(node)
            self._double_link(old_parent)
        parent[self.CHILDREN].insert(index, node)
        self._double_link(parent)
    def insert(self, label, value, parent, index):
        new_node = [label, value, []]
        parent[self.CHILDREN].insert(index, new_node)
        self._double_link(parent)
        return new_node
    def delete(self, node):
        parent = self.get_parent(node)
        del self._parents[id(node)]
        parent[self.CHILDREN].remove(node)
        self._double_link(parent)
    def update(self, node, val):
        node[self.VALUE] = val
    def deep_copy(self):
        def _deep_copy(node):
            children = []
            for n in node[self.CHILDREN]:
                children.append(_deep_copy(n))
            return node[:-1] + [children]
        return ListTreeIface(_deep_copy(self._tree))


