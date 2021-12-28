import unittest
import coinmarketcap
import warnings


class TestCoinmarketcap(unittest.TestCase):

    def test_read_mc_fdmc(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        result = coinmarketcap.read_mc_fdmc('11181,5462')
        self.assertIn('11181', result)
        self.assertIn('5462', result)

        self.assertRaises(Exception, lambda:coinmarketcap.read_mc_fdmc('55555555'))


if __name__ == '__main__':
    unittest.main(0)
