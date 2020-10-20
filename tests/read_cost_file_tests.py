import unittest

import cost_file_reader as cost_reader
import instance_allocator


class CostFileTestCases(unittest.TestCase):

    # Read costs tests
    def test_non_existing_file_returns_error(self):
        self.assertEqual(cost_reader.read_cost('invalid_file.json'), {"ERROR": "File not found"})

    def test_existing_file_returns_contents(self):
        self.assertEqual(cost_reader.read_cost('test_cost_file_valid_data.json'),
                         {'us-east': {'large': 0.12, 'xlarge': 0.23, '2xlarge': 0.45}})

    def test_existing_file_invalid_data_returns_invalid_data_error(self):
        self.assertEqual(cost_reader.read_cost('test_cost_file_invalid_data.json'), {"ERROR": "Invalid input data"})


class InstanceAllocatorTests(unittest.TestCase):

    def setUp(self):
        self.region_dict = cost_reader.read_cost('./test_cost_file_valid_data.json')

    # Instance allocator for max price and hours only
    def test_getting_instance_count_for_valid_hours_and_valid_max_price_returns_proper_output(self):
        self.assertEqual(instance_allocator.instances_for_given_hour(self.region_dict, 3, 5), [{'region': 'us-east',
                                                                                                'total_cost': '$4.800000000000001',
                                                                                                'servers': [
                                                                                                    ('large', 2),
                                                                                                    ('xlarge', 2), (
                                                                                                        '2xlarge',
                                                                                                        2)]}])

    def test_getting_instance_count_for_zero_hours_returns_error(self):
        self.assertEqual(instance_allocator.instances_for_given_hour(self.region_dict, 0, 1), [{'ERROR': "Price and/or "
                                                                                                         "cost must be "
                                                                                                         "greater than "
                                                                                                         "zero"}])


if __name__ == '__main__':
    unittest.main()
