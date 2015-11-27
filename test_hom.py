#!/usr/bin/python

import unittest

import operator

import hom


class Bit(object):
    def __init__(self, value):
        self.value = value
    def get_value(self):
        return self.value
    def set_value(self, value):
        self.value = value
    def __cmp__(self, other):
        return cmp(self.value, other.value)


class TestHOM(unittest.TestCase):
    def setUp(self):
        self.raw_bits = (True, True, False)
        self.raw_texts = ("Kuk", "Kuk", "Puk", "Puk")
        self.bits = [Bit(i) for i in self.raw_bits]
        self.texts = [Bit(i) for i in self.raw_texts]
        self.numbers = [Bit(i) for i in range(10)]

    def test_select(self):
        seq = hom.select(self.bits).get_value()
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(len(seq), 2)

        seq = hom.select(self.bits, False).get_value()
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(len(seq), 1)

        seq = hom.select(self.texts, "Kuk").get_value()
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(len(seq), 2)

        seq = hom.select(self.texts, "NNN").get_value()
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(len(seq), 0)

        seq = hom.select(self.numbers, 6).get_value()
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(len(seq), 1)

        seq = hom.select(self.numbers, 6, operator.gt).get_value()
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(len(seq), 3)

    def test_collect(self):
        seq = hom.collect(self.bits).get_value()
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(list(seq), list(self.raw_bits))

        seq = hom.collect(self.texts).get_value()
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(list(seq), list(self.raw_texts))

        seq = hom.collect(self.numbers).get_value()
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(list(seq), range(10))

    def test_do(self):
        ref = [Bit(True) for i in range(len(self.bits))]
        hom.do(self.bits).set_value(True)
        self.assertEqual(list(self.bits), ref)

        ref = [Bit("bum") for i in range(len(self.texts))]
        hom.do(self.texts).set_value("bum")
        self.assertEqual(list(self.texts), ref)

        ref = [Bit(7) for i in range(10)]
        hom.do(self.numbers).set_value(7)
        self.assertEqual(list(self.numbers), ref)

    def test_chain(self):
        ref = [Bit(0)] + [Bit(7) for i in range(9)]
        seq = hom.list(self.numbers).select(1, operator.ge).get_value()
        seq.do().set_value(7)
        self.assertEqual(list(self.numbers), ref)

if __name__ == "__main__":
    unittest.main()
