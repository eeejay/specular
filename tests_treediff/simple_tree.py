#!/usr/bin/python

import unittest
from treediff import TreeMatcher
from treediff.script_store import ScriptOp

T1 = ['D', None, [
            ['P', None, [
                            ['S', 'a', []],
                            ['S', 'b', []],
                            ['S', 'c', []]]],
            ['P', None, [
                            ['S', 'd', []],
                            ['S', 'e', []]]], 
            ['P', None, [
                            ['S', 'f', []]]]]]

T2 = ['D', None, [
            ['P', None, [
                            ['S', 'a', []],
                            ['S', 'c', []]]],
            ['P', None, [
                            ['S', 'f', []]]],
            ['P', None, [
                            ['S', 'd', []],
                            ['S', 'e', []],
                            ['S', 'g', []]]]]]

EXPECTED_OPS = [
    ScriptOp(ScriptOp.MOVE, 
             'D:[1]/P:None', 'D:None', 4),
    ScriptOp(ScriptOp.INSERT, 
             'D:[2]/P:[2]/S:g', 'S', 'g', 'D:[2]/P:None', 3),
    ScriptOp(ScriptOp.DELETE, 
             'D:[0]/P:[1]/S:b')]

class TestSimpleTree(unittest.TestCase):
    def testtreediff(self):
        matcher = TreeMatcher(T1, T2)
        s = matcher.get_opcodes()
        
        #for o in s: print o
            
        self.assertEqual(len(s), len(EXPECTED_OPS), 
                         "Script has unexpected length.")

        for op, expected in zip(s, EXPECTED_OPS):
            self.assertEqual((op.op_type, op.args), 
                             (expected.op_type, expected.args),
                             "Op types don't match. "
                             "Expected %s, got %s" % (expected, op))

        self.assertEqual(len(matcher.get_opcodes()), 0,
                         "Script is not accurate")

if __name__ == '__main__':
    unittest.main()
