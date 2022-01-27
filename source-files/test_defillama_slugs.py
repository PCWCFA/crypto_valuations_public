import unittest
import defillama_slugs
import warnings


class TestDefillamaSlugs(unittest.TestCase):

    def test_get_protocols_and_chains(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        result = defillama_slugs.get_protocols_and_chains()
        # assert that number of protocols = number of protocols matched by cmcId + number of protocols without cmcId +
        # number of protocols with cmcId that can't be matched to coinmarketcap reference data
        self.assertEqual(result[0], result[1] + result[2] + result[3])
        # assert that number of chains = number of chains matched by cmcId + number of chains without cmcId +
        # number of chains with cmcId that can't be matched to coinmarketcap reference data
        self.assertEqual(result[4], result[5] + result[6] + result[7])


if __name__ == '__main__':
    unittest.main(0)
