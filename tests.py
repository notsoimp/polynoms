import unittest
from polynomial import Polynomial


class TestParsers(unittest.TestCase):
    def test_is_correct(self):
        self.assertTrue(Polynomial.is_correct(Polynomial('2x^2 + 3xy')))
        self.assertTrue(Polynomial.is_correct(Polynomial('2 * x ^ 2')))
        self.assertTrue(Polynomial.is_correct(Polynomial('(15x)(13z^3+2)')))
        self.assertFalse(Polynomial.is_correct(Polynomial('(15x')))
        self.assertFalse(Polynomial.is_correct(Polynomial('25^x')))
        self.assertFalse(Polynomial.is_correct(Polynomial('x^*5')))

    def test_init_dict(self):
        self.assertEqual(Polynomial.init_var_deg_dict(Polynomial('2xy'), '2xy'),
                         {'_': '2', 'x': '1', 'y': '1'})
        self.assertEqual(Polynomial.init_var_deg_dict(Polynomial('2xy+3z'), 'x^2y'),
                         {'_': '1', 'x': '2', 'y': '1', 'z': ''})
        self.assertEqual(Polynomial.init_var_deg_dict(Polynomial('x^3*y^3'), 'x^3*y^3'),
                         {'x': '3', 'y': '3', '_': '1'})
        self.assertEqual(Polynomial.init_var_deg_dict(Polynomial('-x^2'), '-x^2'),
                         {'x': '2', '_': '-1'})
        self.assertEqual(Polynomial.init_var_deg_dict(Polynomial('2'), '2'), {'_': '2'})

    def test_split_polynom(self):
        self.assertEqual(Polynomial.split_polynom_to_dict(Polynomial('2xy')),
                         {(1, 1): 2})
        self.assertEqual(Polynomial.split_polynom_to_dict(Polynomial('2x^3y^4')),
                         {(3, 4): 2})
        self.assertEqual(Polynomial.split_polynom_to_dict(Polynomial('x^3+ 15x^8')),
                         {(3,): 1, (8,): 15})
        self.assertEqual(Polynomial.split_polynom_to_dict(Polynomial('15x^10*y^3 - z^4')),
                         {(10, 3, 0): 15, (0, 0, 4): -1})

    def test_is_equal(self):
        self.assertTrue(Polynomial('2x^2-2x+2') == Polynomial('-2x+2x^2+2'))
        self.assertTrue(Polynomial('2x-2x') == Polynomial('0'))
        self.assertTrue(Polynomial('15xy+25x^2y^2') == Polynomial('15yx+25y^2*x^2'))


if __name__ == '__main__':
    unittest.main()
