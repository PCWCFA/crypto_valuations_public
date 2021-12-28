import unittest
import defillama


class TestDefillama(unittest.TestCase):

    def test_read_protocol_tvl(self):
        result = defillama.read_protocol_tvl('Uniswap')
        self.assertAlmostEqual(result, 8.99, 2)

        self.assertRaises(Exception, lambda: defillama.read_protocol_tvl('Eunuchswap'))

    def test_read_chain_tvl(self):
        result = defillama.read_chain_tvl('Solana')
        self.assertAlmostEqual(result, 12.00, 0)

        self.assertRaises(Exception, lambda: defillama.read_chain_tvl('Solano'))


if __name__ == '__main__':
    unittest.main(0)
