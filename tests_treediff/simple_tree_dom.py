#!/usr/bin/python

import unittest
from treediff import DomTreeMatcher
from treediff.script_store import ScriptOp
from xml.dom.minidom import parseString

T1 = '<D><P><S>a</S><S>b</S><S>c</S></P><P alt="bar"><S>d</S><S>e</S></P><P><S>f</S></P></D>'

T2 = '<D><P><S>a</S><S>c</S></P><P><S>f</S></P><P alt="foo"><S>d</S><S>e</S><S>g</S></P></D>'

EXPECTED_OPS = [
    ScriptOp(
        ScriptOp.MOVE, 
        u'/D[1]/P[2]', u'/D[1]', 4),
    ScriptOp(
        ScriptOp.INSERT, 
        u'/D[1]/P[3]/S[3]', u'1~S', None, u'/D[1]/P[3]', 3),
    ScriptOp(
        ScriptOp.UPDATE,
        u'/D[1]/P[3]/@alt', u'foo'),
    ScriptOp(
        ScriptOp.INSERT, 
        u'/D[1]/P[3]/S[3]/text()', '3~#text', u'g', u'/D[1]/P[3]/S[3]', 1),
    ScriptOp(
        ScriptOp.DELETE, 
        u'/D[1]/P[1]/S[2]/text()'),
    ScriptOp(
        ScriptOp.DELETE, 
        u'/D[1]/P[1]/S[2]')]

class TestSimpleTree(unittest.TestCase):
    def testtreescript(self):
        matcher = DomTreeMatcher(parseString(T1), parseString(T2))
        s = matcher.get_opcodes()
        
        #for o in s: print o
        
        self.assertEqual(len(s), len(EXPECTED_OPS), 
                         "Script has unexpected length.\n%s" %
                         '\n'.join(map(str, s)))

        for op, expected in zip(s, EXPECTED_OPS):
            self.assertEqual((op.op_type, op.args), 
                             (expected.op_type, expected.args),
                             "Op types don't match. "
                             "Expected %s, got %s" % (expected, op))
    
        
        self.assertEqual(len(matcher.get_opcodes()), 0,
                         "Script is not accurate")
        

if __name__ == '__main__':
    unittest.main()
