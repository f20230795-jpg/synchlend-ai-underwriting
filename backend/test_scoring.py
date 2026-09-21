import unittest
from scoring import calculate_ntc_score

class TestNTCScoringEngine(unittest.TestCase):
    def test_valid_approval(self):
        risk, sent, dec, exp = calculate_ntc_score(15000, 4000, 750, 10000, "Full time engineer")
        self.assertEqual(dec, "APPROVED")

    def test_high_risk_rejection(self):
        risk, sent, dec, exp = calculate_ntc_score(5000, 4000, 300, 50000, "Erratic gig work")
        self.assertEqual(dec, "DECLINED")

    def test_high_dti(self):
        risk, sent, dec, exp = calculate_ntc_score(4000, 3500, 600, 20000, "Stable job")
        self.assertEqual(dec, "DECLINED")
        self.assertIn("DTI", exp)

    def test_negative_cash_flow(self):
        risk, sent, dec, exp = calculate_ntc_score(3000, 3000, 700, 5000, "Salaried")
        self.assertEqual(dec, "DECLINED")

    def test_invalid_strings(self):
        risk, sent, dec, exp = calculate_ntc_score("pizza", 4000, 700, 5000, "Salaried")
        self.assertEqual(dec, "DECLINED")
        self.assertIn("Error", exp)

if __name__ == '__main__':
    unittest.main()