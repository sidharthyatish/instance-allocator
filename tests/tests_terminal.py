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
        self.instance_dict = {"large": 1, "xlarge": 2, "2xlarge": 4, "4xlarge": 8, "8xlarge": 16, "10xlarge": 32}

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

    def test_correct_number_of_cpus_have_been_allocated_for_requested_cpu_count(self):
        requested_num_of_cpu = 5
        result = instance_allocator.instances_for_given_cpu_count(self.region_dict, 5, requested_num_of_cpu)[0]
        server_list = result['servers']
        allocated_cpu = 0
        for each_server in server_list:
            allocated_cpu = allocated_cpu + each_server[1] * self.instance_dict[each_server[0]]
        self.assertEqual(requested_num_of_cpu, allocated_cpu)

        # Instance allocator with given number of CPUs and max price for certain hours

    def test_getting_instance_count_for_valid_hours_and_valid_cpu_count_with_valid_price_returns_proper_output(
            self):
        self.assertEqual(instance_allocator.instances_for_given_cpu_and_price(self.region_dict, 3, 6, 3),
                         [{'region': 'us-east',
                           'servers': [('xlarge', 1), ('2xlarge', 1)],
                           'total_cost': '$2.04'}])

    def test_getting_instance_count_for_invalid_price_or_invalid_count_or_invalid_hours_returns_error(self):
        self.assertEqual(instance_allocator.instances_for_given_cpu_and_price(self.region_dict, 0, 4, 0),
                         [{'ERROR': 'Hours, CPU count and price must be greater than zero'}])

    def test_equal_number_of_cpus_have_been_allocated_for_requested_cpu_count_despite_varied_costs(self):
        requested_num_of_cpu = 10
        result_1 = instance_allocator.instances_for_given_cpu_and_price(self.region_dict, 5, requested_num_of_cpu, 10)[
            0]
        result_2 = instance_allocator.instances_for_given_cpu_and_price(self.region_dict, 5, requested_num_of_cpu, 20)[
            0]
        server_list_1 = result_1['servers']
        server_list_2 = result_2['servers']
        allocated_cpu_1 = 0
        allocated_cpu_2 = 0

        for each_server in server_list_1:
            allocated_cpu_1 = allocated_cpu_1 + each_server[1] * self.instance_dict[each_server[0]]

        for each_server in server_list_2:
            allocated_cpu_2 = allocated_cpu_2 + each_server[1] * self.instance_dict[each_server[0]]
        self.assertEqual(allocated_cpu_1, allocated_cpu_2)


if __name__ == '__main__':
    unittest.main()
