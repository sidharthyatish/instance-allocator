import unittest

import cost_file_reader as cost_reader


class MyTestCase(unittest.TestCase):

    def test_invalid_file_returns_error(self):
        self.assertEqual(cost_reader.read_cost('invalid_file.json'), {"ERROR": "File not found"})

    def test_valid_file_returns_contents(self):
        self.assertEqual(cost_reader.read_cost('test_cost_file_valid_data.json'),
                         {'us-east': {'large': 0.12, 'xlarge': 0.23, '2xlarge': 0.45}})

    def test_valid_file_invalid_data_returns_invalid_data_error(self):
        self.assertEqual(cost_reader.read_cost('test_cost_file_invalid_data.json'), {"ERROR": "Invalid input data"})


if __name__ == '__main__':
    unittest.main()
