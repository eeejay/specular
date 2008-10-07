from difflib import SequenceMatcher
from script_store import ScriptStore
from tree_iface import ListTreeIface

class TreeMatcher:
    def __init__(self, tree1, tree2, f=0.6, t=0.5, 
                 tree_parser=ListTreeIface, script_store=ScriptStore):
        self._tree1 = tree_parser(tree1)
        self._tree2 = tree_parser(tree2)
        self._script_store = script_store
        self._f = f
        self._t = t

    def get_opcodes(self):
        self._match()
        return self._do_fmes()

    def print_mapping(self):
        for n1, n2 in self._mapping:
            print '%s\t\t\t%s' % (self._tree1.node_repr(n1), 
                              self._tree2.node_repr(n2))

    def _get_partner_in_t1(self, node):
        for n1, n2 in self._mapping:
            if id(n2) == id(node):
                return n1
        return None

    def _get_partner_in_t2(self, node):
        for n1, n2 in self._mapping:
            if id(n1) == id(node):
                return n2
        return None

    def _find_pos(self, x):
        y = self._tree2.get_parent(x)
        left_of_ordered = filter(
            lambda n: self._tree2.is_ordered(n), 
            self._tree2.get_children(y)[:self._tree2.get_index_in_parent(x)])
        if (self._tree2.is_ordered(x) and not left_of_ordered) or \
                not left_of_ordered:
            # x is the leftmost child that is marked "in order".
            return 1
        v = left_of_ordered[-1]
        u = self._get_partner_in_t1(v) # v is in tree 2
        return self._tree1.get_index_in_parent(u) + 2

    def _align_children(self, w, x, scrpt):
        # mark all children of w and x and "not in order"
        self._tree1.mark_children_unordered(w)
        self._tree2.mark_children_unordered(x)
        s1 = filter(lambda n: self._get_partner_in_t2(n) in self._tree2.get_children(x), 
                    self._tree1.get_children(w)) # n is in tree 1
        s2 = filter(lambda n: self._get_partner_in_t1(n) in self._tree1.get_children(w), 
                    self._tree2.get_children(x))  # n is in tree 2
        s = self._lcs(s1, s2, lambda n1, n2: (n1, n2) in self._mapping)
        for a, b in s:
            self._tree1.mark_ordered(a, True)
            self._tree2.mark_ordered(b, True)
        for a in s1:
            b = self._get_partner_in_t2(a) # a is in tree 1
            if (a, b) in self._mapping and (a, b) not in s:
            #if False:
                self._tree1.mark_ordered(a, True)
                self._tree2.mark_ordered(b, True)
                k = self._find_pos(b)
                scrpt.move(a, w, k)
                self._tree1.move(a, w, k)
        return scrpt

    def _do_fmes(self):
        scrpt = self._script_store(self._tree1)
        # Breadth first traversal of T2
        for x in self._tree2.nodes_breadth():
            y = self._tree2.get_parent(x)
            z = self._get_partner_in_t1(y) # y is in tree 2
            w = self._get_partner_in_t1(x) # x is in tree 2
            if not w:
                self._tree2.mark_ordered(x, True)
                k = self._find_pos(x)
                w = self._tree1.insert(
                    self._tree2.get_label(x), self._tree2.get_value(x), z, k)
                scrpt.insert(w, self._tree2.get_label(x), self._tree2.get_value(x), z, k)
                self._map(w, x)    
                self._tree1.mark_ordered(w, True)
            elif y is not None:
                v = self._tree1.get_parent(w)
                if self._tree2.get_value(x) != self._tree1.get_value(w):
                    scrpt.update(w, self._tree2.get_value(x))
                    self._tree1.update(w, self._tree2.get_value(x))
                if v != z:
                    self._tree2.mark_ordered(x, True)
                    k = self._find_pos(x)
                    scrpt.move(w, z, k)
                    self._tree1.move(w, z, k)
                    self._tree1.mark_ordered(w, True)
            self._align_children(w, x, scrpt)
        # Depth traversal of T1
        for w in self._tree1.nodes_postorder():
            if not self._get_partner_in_t2(w): # w is in tree 1
                scrpt.delete(w)
                self._tree1.delete(w)
        return scrpt

    def _match(self):
        self._mapping = []
        unmatched1, unmatched2 = [], []
        leaf_labels1, middle_labels1 = self._tree1.get_labels()
        leaf_labels2, middle_labels2 = self._tree2.get_labels()
        self._map(self._tree1.get_root(), self._tree2.get_root())
        for equal, labels1, labels2 in \
                ((self._leaf_equal, leaf_labels1, leaf_labels2),
                 (self._middle_equal, middle_labels1, middle_labels2)):
            label_set = set(labels1.keys()).intersection(set(labels2.keys()))
            for l in label_set:
                s1 = labels1[l]
                s2 = labels2[l]
                common = self._lcs(s1, s2, equal)
                for n1, n2 in common:
                    s1.remove(n1)
                    s2.remove(n2)
                    self._map(n1, n2)
                for n1, n2 in [(x,y) for x in s1 for y in s2]:
                    if equal(n1, n2) and \
                            not self._tree1.is_mapped(n1) \
                            and not self._tree2.is_mapped(n2):
                        self._map(n1, n2)
                unmatched1 += s1
                unmatched2 += s2
        return unmatched1, unmatched2

    def _map(self, n1, n2):
        self._mapping.append((n1, n2))
        self._tree1.mark_mapped(n1)
        self._tree1.cache_pedigree(n1)
        self._tree2.cache_pedigree(n2)
    
    def _leaf_equal(self, node1, node2):
        sm = SequenceMatcher(None, 
                             self._tree1.get_value(node1) or '', 
                             self._tree2.get_value(node2) or '')
        return sm.quick_ratio() > self._f

    def quick_ratio(self, a,b):
        """
        optimized version of the standard difflib.py quick_ration
        (without junk and class)
        Return an upper bound on ratio() relatively quickly.
        """
        # viewing a and b as multisets, set matches to the cardinality
        # of their intersection; this counts the number of matches
        # without regard to order, so is clearly an upper bound
        if not a and not b:
            return 1
        fullbcount = {}
        for elt in b:
            fullbcount[elt] = fullbcount.get(elt, 0) + 1
        # avail[x] is the number of times x appears in 'b' less the
        # number of times we've seen it in 'a' so far ... kinda
        avail = {}
        availhas, matches = avail.has_key, 0
        for elt in a:
            if availhas(elt):
                numb = avail[elt]
            else:
                numb = fullbcount.get(elt, 0)
            avail[elt] = numb - 1
            if numb > 0:
                matches = matches + 1
        return 2.0 * matches / (len(a) + len(b))


    def _middle_equal(self, node1, node2):
        def _have_matching_ancestor(n1, n2):
            return self._tree1.is_descendant(n1, node1) and \
                self._tree2.is_descendant(n2, node2)
        length = len(
            filter(
                    lambda x: _have_matching_ancestor(x[0], x[1]),
                    self._mapping))
        max_descendants = max(self._tree1.get_descendant_count(node1),
                              self._tree2.get_descendant_count(node2))
        factor = 2.5*length/float(max_descendants)
        return factor >= self._t

    def _lcs(self, X, Y, equal):
        """
        apply the greedy lcs/ses algorithm between X and Y sequence
        (should be any Python's sequence)
        equal is a function to compare X and Y which must return 0 if
        X and Y are different, 1 if they are identical
        return a list of matched pairs in tuplesthe greedy lcs/ses algorithm
        """
        N, M = len(X), len(Y)
        if not X or not Y :
            return []
        max = N + M
        v = [0 for i in xrange(2*max+1)]
        common = [[] for i in xrange(2*max+1)]
        for D in xrange(max+1):
            for k in xrange(-D, D+1, 2):
                if k == -D or k != D and v[k-1] < v[k+1]:
                    x = v[k+1]
                    common[k] = common[k+1][:]
                else:
                    x = v[k-1] + 1
                    common[k] = common[k-1][:]

                y = x - k
                while x < N and y < M and equal(X[x], Y[y]):
                    common[k].append((x, y))
                    x += 1 ; y += 1
                v[k] = x
                if x >= N and y >= M:
                    return [ (X[x],Y[y]) for x,y in common[k] ]

