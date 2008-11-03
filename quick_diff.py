#!/usr/bin/env python
#
# Speclenium Test harness
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
#
# The Initial Developer of the Original Code is Eitan Isaacson.
# Portions created by the Initial Developer are Copyright (C) 2008
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Original Author: Eitan Isaacson (eitan@ascender.com)
#
# Alternatively, the contents of this file may be used under the terms of
# either of the GNU General Public License Version 2 or later (the "GPL"),
# or the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.

from speclenium_client import SpecleniumClient as selenium
import sys, codecs
from xml.dom.minidom import parse, parseString
from ConfigParser import ConfigParser
import treediff
from treediff.dom_tree_iface import DomTreeIface
from difflib import SequenceMatcher
from treediff.dom_tree_iface import strip_whitespace
from urlparse import urlparse

class AccessibleChangesScriptStore(treediff.MarkChangesScriptStore):
    def __init__(self, tree):
        self.simple_ops = []
        self._simple_inserted = []
        treediff.MarkChangesScriptStore.__init__(self, tree)


    def move(self, node, parent, index):
        self.simple_ops.append('Move %s to %s (%s)' % \
                                   (self._tree.node_repr(node),
                                    self._tree.node_repr(parent), index))
        treediff.MarkChangesScriptStore.move(self, node, parent, index)
    
    def update(self, node, value):
        self.simple_ops.append('Update %s to %s' % \
                                   (self._tree.node_repr(node), value))
        treediff.MarkChangesScriptStore.update(self, node, value)

    def insert(self, node, label, value, parent, index):
        if node.nodeType == node.ATTRIBUTE_NODE:
            element = node.ownerElement
            if element.hasAttribute('role') and \
                    element.hasAttribute('name') and \
                    element not in self._simple_inserted:
                self.simple_ops.append('Inserted %s' % \
                                           self._tree.node_repr(element))
                self._simple_inserted.append(element)
        treediff.MarkChangesScriptStore.insert(
            self, node, label, value, parent, index)

    def delete(self, node):
        if node.nodeType != node.ATTRIBUTE_NODE:
            self.simple_ops.append('Delete %s' % \
                                       self._orig_tree.node_repr(self._pairs[node]))
        treediff.MarkChangesScriptStore.delete(self, node)


class AccessibleTreeIface(DomTreeIface):
    def get_labels(self):
        def _get_labels(node, middle_labels, leaf_labels):
            if node and node.childNodes:
                for n in node.childNodes:
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

    def node_repr(self, node):
        p = node
        path = []
        while p:
            if p.nodeType == p.ATTRIBUTE_NODE:
                lname = '@' + self.get_label(p).split('~',1)[-1]
            elif p.nodeType == p.TEXT_NODE:
                lname = 'text()'
            else:
                lname = '[%s|%s](%d)' % (p.getAttribute('name'),
                                         p.getAttribute('role'),
                                         self.get_index_in_parent(p, True) + 1)
            path.insert(0, lname)
            p = self.get_parent(p)
        return '/'+'/'.join(path)
    def deep_copy(self):
        return AccessibleTreeIface(self._dom.cloneNode(True))

class AccessibleTreeMatcher(treediff.DomTreeMatcher):
    def __init__(self, tree1, tree2, f=0.75, t=0.5, 
                 tree_parser=AccessibleTreeIface, 
                 script_store=AccessibleChangesScriptStore):
        tree1 = parseString(tree1.documentElement.lastChild.toxml())
        tree2 = parseString(tree2.documentElement.lastChild.toxml())
        treediff.DomTreeMatcher.__init__(
            self, tree1, tree2, f, t, tree_parser, script_store)

    def _get_joint_value(self, node):
        keys = node.attributes.keys()
        keys.sort()
        return ','.join(node.attributes[k].value for k in keys)

    def _leaf_equal(self, node1, node2):
        val1 = self._get_joint_value(node1)
        val2 = self._get_joint_value(node2)
        sm = SequenceMatcher(None, val1, val2)
        return sm.ratio() > self._f

    def _map(self, n1, n2):
        self._mapping.append((n1, n2))
        self._tree1.mark_mapped(n1)
        self._tree1.cache_pedigree(n1)
        self._tree2.cache_pedigree(n2)
        if getattr(n1, 'attributes', None) and getattr(n2, 'attributes', None):
            for attrib in set(n1.attributes.keys() + n2.attributes.keys()):
                a1 = n1.attributes.get(attrib)
                a2 = n2.attributes.get(attrib)
                if None not in (a1, a2):
                    self._map(a1, a2)
                

def get_acc_tree(profile_name,host, command, url):
    parsed = urlparse(url)
    try:
        first_half = url.split(parsed[2])[0]
        second_half = url.split(parsed[1])[-1]
    except:
        first_half = url
        second_half = '/'
    s = selenium(host, 4444, command, first_half)
    s.start()
    s.set_timeout(30000)
    s.open(second_half)
    s.window_maximize()
    x = s.get_accessible_doc()
    s.stop()
    return parseString('<tree><title>%s</title>%s</tree>' % 
                       (profile_name, x.encode('utf-8')))

def browser_cb(option, opt_str, value, parser):
    browsers = value.split(',')
    acc_trees = getattr(parser.values, 'acc_trees', [])
    if len(acc_trees) + len(browsers) > 2:
        raise OptionValueError("Cannot compare more than two browsers/files")
    for b in browsers:
        acc_trees.append(b)
    parser.values.acc_trees = acc_trees
        

def file_cb(option, opt_str, value, parser):
    files = value.split(',')
    acc_trees = getattr(parser.values, 'acc_trees', [])
    if len(acc_trees) + len(files) > 2:
        raise OptionValueError("Cannot compare more than two browsers/files")
    for f in files:
        d = parse(f)
        strip_whitespace(d)
        acc_trees.append(d)
    parser.values.acc_trees = acc_trees

def _get_tree_title(tree):
    title_tags = tree.getElementsByTagName('title')
    if not title_tags:
        return ''
    return title_tags[0].firstChild.data.strip()

if __name__ == '__main__':
    from optparse import OptionParser
    from sys import stderr, stdout

    usage = "Usage: %prog [options] url"
    parser = OptionParser(usage)
    parser.add_option("--list-agents", dest="list_agents",
                      action="store_true", help="list available user agents")
    parser.add_option("-B", "--browser", action="callback", type="string", 
                      callback=browser_cb,
                      help="browser to run")
    parser.add_option("-F", "--file", action="callback", type="string", 
                      callback=file_cb, 
                      help="XML accessible tree file")
    parser.add_option("-c", "--config", dest="cfg_file",
                      action="store", help="config file", 
                      default="settings.ini")
    parser.add_option("-o", "--output", dest="output",
                      action="store", 
                      help="output XML. Single tree or side-by-side.")
    parser.add_option("--print-changes", dest="print_changes",
                      action="store_true", help="print tree changes")

    (options, args) = parser.parse_args()
    cfg = ConfigParser()
    cfg.read(options.cfg_file)
    if options.list_agents:
        print 'Available user agents:'
        for section in cfg.sections():
            print ' %s' % section
    else:
        acc_trees = getattr(options, "acc_trees", [])
        if len(acc_trees) > 2:
            raise OptionValueError(
                "Need exactly two browsers/files for comparison")
        for i in xrange(len(acc_trees)):
            if type(acc_trees[i]) == str:
                acc_trees[i] = get_acc_tree(
                    acc_trees[i],
                    cfg.get(acc_trees[i], 'host'), 
                    cfg.get(acc_trees[i], 'command'),
                    args[0])

        if len(acc_trees) == 2:
            tm = AccessibleTreeMatcher(*options.acc_trees)
            print >>stderr, "Got trees. Retrieving delta..."
            s = tm.get_opcodes()
            if options.print_changes:
                print '\n'.join(s.simple_ops)
            if options.output:
                f = open(options.output, 'w')
                title1 = _get_tree_title(options.acc_trees[0])
                title2 = _get_tree_title(options.acc_trees[1])
                doc = s.get_sidebyside("%s vs. %s" % (title1, title2))
                doc.getElementsByTagName('left')[0].setAttribute(
                    "profile", title1)
                doc.getElementsByTagName('right')[0].setAttribute(
                    "profile", title2)
                doc.insertBefore(
                    doc.createProcessingInstruction(
                        'xml-stylesheet', 
                        'type="text/xsl" href="api-compare.xsl"'),
                    doc.documentElement)
                f.write(doc.toprettyxml('  ').encode('utf-8'))
                f.close()
        elif len(acc_trees) == 1:
            # Just output accessible tree
            if options.output:
                out = open(options.output, 'w')
            else:
                out = stdout
            out.write(acc_trees[0].toprettyxml('  ').encode('utf-8'))
            out.close()
