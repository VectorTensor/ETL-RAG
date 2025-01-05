import unittest

from generate_fake_transaction_data import generate_fake_sales_data


class TestGenerateListFunction(unittest.TestCase):
    def test_generate_list_size(self):
        # Define test cases
        test_cases = [0, 1, 5, 10, 100]

        for size in test_cases:
            with self.subTest(size=size):
                result = generate_fake_sales_data(size)
                # Check if the result is a list
                self.assertIsInstance(result, list, f"Expected a list but got {type(result)}")
                # Check if the size matches the input
                self.assertEqual(len(result), size, f"Expected list of size {size} but got {len(result)}")


