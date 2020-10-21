import unittest

import cost_file_reader as cost_reader
import instance_allocator


class CostFileTestCases(unittest.TestCase):

    # Read costs tests
    def test_non_existing_file_returns_error(self):
        self.assertEqual(cost_reader.read_cost('invalid_file.json'), {"ERROR": "File not found"})

    def test_existing_file_returns_contents(self):
        self.assertEqual(cost_reader.read_cost('tests/test_cost_file_valid_data.json'),
                         {'us-east': {'large': 0.12, 'xlarge': 0.23, '2xlarge': 0.45}})

    def test_existing_file_invalid_data_returns_invalid_data_error(self):
        self.assertEqual(cost_reader.read_cost('tests/test_cost_file_invalid_data.json'), {"ERROR": "Invalid input data"})


class InstanceAllocatorTests(unittest.TestCase):

    def setUp(self):
        self.region_dict = cost_reader.read_cost('tests/test_cost_file_valid_data.json')

    # Instance allocator for max price and hours only
    def test_getting_instance_count_for_valid_hours_and_valid_max_price_returns_proper_output(self):
        self.assertEqual(instance_allocator.instances_for_given_price(self.region_dict, 3, 5), [{'region': 'us-east',
                                                                                                'total_cost': '$4.8',
                                                                                                'servers': [
                                                                                                    ('large', 2),
                                                                                                    ('xlarge', 2), (
                                                                                                        '2xlarge',
                                                                                                        2)]}])

    def test_getting_instance_count_for_zero_hours_returns_error(self):
        self.assertEqual(instance_allocator.instances_for_given_price(self.region_dict, 0, 1), [{'ERROR': "Hours and/or "
                                                                                                         "cost must be "
                                                                                                         "greater than "
                                                                                                         "zero"}])

    def test_getting_instance_count_for_negative_hours_returns_error(self):
        self.assertEqual(instance_allocator.instances_for_given_price(self.region_dict, -1, 1),
                         [{'ERROR': "Hours and/or "
                                    "cost must be "
                                    "greater than "
                                    "zero"}])

    def test_getting_instance_count_for_zero_price_returns_error(self):
        self.assertEqual(instance_allocator.instances_for_given_price(self.region_dict, 10, 0),
                         [{'ERROR': "Hours and/or "
                                    "cost must be "
                                    "greater than "
                                    "zero"}])

    def test_getting_instance_count_for_negative_price_returns_error(self):
        self.assertEqual(instance_allocator.instances_for_given_price(self.region_dict, 5, -1),
                         [{'ERROR': "Hours and/or "
                                    "cost must be "
                                    "greater than "
                                    "zero"}])

    # Instance allocator given number of CPUs and hours
    def test_getting_instance_count_for_valid_hours_and_valid_cpu_count_returns_proper_output(self):
        self.assertEqual(instance_allocator.instances_for_given_cpu_count(self.region_dict, 3, 5),
                         [{'region': 'us-east',
                           'servers': [('large', 1), ('2xlarge', 1)],
                           'total_cost': '$1.71'}])

    def test_getting_instance_count_with_valid_cpu_count_for_zero_hours_returns_error(self):
        self.assertEqual(instance_allocator.instances_for_given_cpu_count(self.region_dict, 0, 1),
                         [{'ERROR': "Hours and/or "
                                    "CPU count must be "
                                    "greater than "
                                    "zero"}])

    def test_getting_instance_count_with_valid_cpu_count_for_negative_hours_returns_error(self):
        self.assertEqual(instance_allocator.instances_for_given_cpu_count(self.region_dict, -1, 1),
                         [{'ERROR': "Hours and/or "
                                    "CPU count must be "
                                    "greater than "
                                    "zero"}])

    def test_getting_instance_count_with_valid_hours_and_zero_cpu_returns_error(self):
        self.assertEqual(instance_allocator.instances_for_given_cpu_count(self.region_dict, 3, 0),
                         [{'ERROR': "Hours and/or "
                                    "CPU count must be "
                                    "greater than "
                                    "zero"}])

    def test_getting_instance_count_with_valid_hours_and_negative_cpu_returns_error(self):
        self.assertEqual(instance_allocator.instances_for_given_cpu_count(self.region_dict, 4, -1),
                         [{'ERROR': "Hours and/or "
                                    "CPU count must be "
                                    "greater than "
                                    "zero"}])


if __name__ == '__main__':
    unittest.main()
