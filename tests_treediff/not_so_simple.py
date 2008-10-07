#!/usr/bin/python

import unittest
from treediff import DomTreeMatcher
from treediff.script_store import ScriptOp
from treediff.dom_tree_iface import strip_whitespace
from xml.dom.minidom import parse
import os, os.path
from difflib import unified_diff

srcroot = os.path.abspath(os.path.dirname(__file__)+os.path.sep+os.path.pardir)

xml_file1 = os.path.join(srcroot, 'samples', 'ie.xml')
xml_file2 = os.path.join(srcroot, 'samples', 'firefox3.xml')

class TestSimpleTree(unittest.TestCase):
    def testtreescript(self):
        d1 = parse(xml_file1)
#        strip_whitespace(d1)
        d2 = parse(xml_file2)
#        strip_whitespace(d2)

        matcher = DomTreeMatcher(d1, d2)
        before = matcher._tree1._dom.toprettyxml(' ')
        wanted = matcher._tree2._dom.toprettyxml(' ')
        scrpt = '\n'.join(map(str, matcher.get_opcodes()))
#        matcher._match()
#        for m1, m2 in matcher._mapping:
#            if m1.nodeType == m1.COMMENT_NODE:
#                print m1, m2
        got = matcher._tree1._dom.toprettyxml(' ')
#        print len(s)
#        print len(s)
        print '*'*80
        s = matcher.get_opcodes()
#        s2 = matcher.get_opcodes()
        diagnostics = """
Second run returned a script (%d)
Started with:
%s
%s
Expected:
%s
%s
Got:
%s
%s
Script:
%s
%s
Second run:
%s
%s""" % (len(s), '-'*80, before, '-'*80, 
         wanted, '-'*80, got, '-'*80, scrpt, '-'*80, '\n'.join(map(str, s)))

        print wanted == got
        diagnostics = '\n'.join(map(str, s))
        self.assertEqual(len(s), 0,
                         "Script is not accurate. \n%s" % diagnostics)
        print scrpt

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 3:
        xml_file2 = sys.argv.pop(-1)
        xml_file1 = sys.argv.pop(-1)
    unittest.main()
