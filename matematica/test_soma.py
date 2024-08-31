import unittest
from matematica.soma import somar

class TestSomarFunction(unittest.TestCase):

    def test_somar_two_positive_numbers(self):
        result = somar(3, 5)
        self.assertEqual(result, 8)

    def test_somar_positive_and_negative_number(self):
        result = somar(10, -3)
        self.assertEqual(result, 7)

    def test_somar_two_negative_numbers(self):
        result = somar(-4, -6)
        self.assertEqual(result, -10)

    def test_somar_with_zero(self):
        result = somar(0, 5)
        self.assertEqual(result, 5)

    def test_somar_large_numbers(self):
        result = somar(1000000, 2000000)
        self.assertEqual(result, 3000000)