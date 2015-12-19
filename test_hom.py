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


class Morph(object):
    def get_value(self, morph):
        return morph


class TestHOM(unittest.TestCase):
    def setUp(self):
        self.raw_bits = (True, True, False)
        self.raw_texts = ("Kuk", "Kuk", "Puk", "Puk")
        self.bits = [Bit(i) for i in self.raw_bits]
        self.texts = [Bit(i) for i in self.raw_texts]
        self.numbers = [Bit(i) for i in range(10)]
        self.morphs = [Morph() for i in range(4)]

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

        seq = hom.select(self.morphs).get_value(True)
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(len(seq), 4)

        seq = hom.select(self.morphs).get_value(morph=True)
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(len(seq), 4)

        seq = hom.select(self.bits).value()
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(len(seq), 2)

        seq = hom.select(self.bits, False).value()
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(len(seq), 1)

        seq = hom.select(self.texts, "Kuk").value()
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(len(seq), 2)

        seq = hom.select(self.texts, "NNN").value()
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(len(seq), 0)

        seq = hom.select(self.numbers, 6).value()
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(len(seq), 1)

        seq = hom.select(self.numbers, 6, operator.gt).value()
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

        seq = hom.collect(self.morphs).get_value(1)
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(list(seq), [1 for i in range(4)])

        seq = hom.collect(self.bits).value()
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(list(seq), list(self.raw_bits))

        seq = hom.collect(self.texts).value()
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(list(seq), list(self.raw_texts))

        seq = hom.collect(self.numbers).value()
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(list(seq), range(10))

    def test_do(self):
        ref = [Bit(True) for i in range(len(self.bits))]
        seq = hom.do(self.bits).set_value(True)
        self.assertEqual(list(self.bits), ref)
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(seq, self.bits)

        ref = [Bit("bum") for i in range(len(self.texts))]
        seq = hom.do(self.texts).set_value("bum")
        self.assertEqual(list(self.texts), ref)
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(seq, self.texts)

        ref = [Bit(7) for i in range(10)]
        seq = hom.do(self.numbers).set_value(7)
        self.assertEqual(list(self.numbers), ref)
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(seq, self.numbers)

    def test_reduce(self):
        one = [1, 2]
        two = [3, 4]
        both = [one, two]
        expected = one + two

        result = hom.reduce(both).__add__()
        self.assertEqual(result, expected)

    def test_each(self):
        ref = [Bit, Bit, Bit]
        seq = hom.each(self.bits, type)
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(list(seq), ref)

        seq = hom.list(self.bits).each(type)
        self.assertTrue(isinstance(seq, hom.list))
        self.assertEqual(list(seq), ref)

    def test_chain(self):
        ref = [Bit(0)] + [Bit(7) for i in range(9)]
        seq = hom.list(self.numbers).select(1, operator.ge).get_value()
        seq.do().set_value(7)
        self.assertEqual(list(self.numbers), ref)


if __name__ == "__main__":
    unittest.main()
