class ScriptOp:
    MOVE = 0
    INSERT = 1
    UPDATE = 2
    DELETE = 3
    OP_STRINGS = ['mov', 'ins', 'upd', 'del']
    def __init__(self, op_type, *args):
        self.op_type = op_type
        self.args = args
    def __repr__(self):
        return '%s%s' % (self.OP_STRINGS[self.op_type], self.args)

class ScriptStore(list):
    def __init__(self, tree):
        self._tree = tree
        list.__init__(self)
    def append(self, val):
        list.append(self, val)
    def move(self, node, parent, index):
        self.append(ScriptOp(
                ScriptOp.MOVE, self._tree.node_repr(node), 
                self._tree.node_repr(parent), index))
    def insert(self, node, label, value, parent, index):
        self.append(ScriptOp(
                ScriptOp.INSERT, self._tree.node_repr(node), 
                label, value, self._tree.node_repr(parent), index))
    def update(self, node, value):
        self.append(ScriptOp(
                ScriptOp.UPDATE, self._tree.node_repr(node), value))
    def delete(self, node):
        self.append(ScriptOp(
                ScriptOp.DELETE, self._tree.node_repr(node)))
