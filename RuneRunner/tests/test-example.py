import unittest
from central_llm.central_llm import CentralLLM

class TestCentralLLM(unittest.TestCase):
    def setUp(self):
        self.llm = CentralLLM()

    def test_analyze_market_data(self):
        result = self.llm.analyze_market_data("Test market data")
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
