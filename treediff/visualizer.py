from tree_matcher import TreeMatcher
from sys import stdout
import codecs

class VisualTreeMatcher(TreeMatcher):
    def draw_trees(self, draw_mapping=False, fn=None):
        if fn:
            out = codecs.open(fn, 'w', 'utf-8')
        else:
            out = stdout
        print >>out, 'digraph G {'
        print >>out,'nodesep = 0.3;'
        print >>out,'ranksep = 2;'
        print >>out,'center = 1;'
        self._draw_tree(self._tree1, "Tree 1", out)
        self._draw_tree(self._tree2, "Tree 2", out)
        if draw_mapping:
            for n1, n2 in self._mapping:
                print >>out, '%s -> %s [color=blue,dir=none,style=dashed,constraint=false];' % (id(n1), id(n2))
        print >>out, '}'
        if fn:
            out.close()

    def _draw_tree(self, tree, label, out):
        print >>out, 'subgraph cluster_%s {' % label.lower().replace(' ', '_')
        self._draw_node(tree, tree.get_root(), out)
        print >>out,'label = "%s";' % label
        print >>out,'color = "%s";' % 'black'
        print >>out,'}'

    def _draw_node(self, tree, node, out):
        print >>out, '%s [label="%s(%s)"]' % \
            (id(node), tree.get_label(node), (tree.get_value(node) or '').replace('\n', ''))
        for n in tree.get_children(node):
            print >>out, '%s -> %s [weight=0];' % (id(node), id(n))
            self._draw_node(tree, n, out)
