from cost_file_reader import read_cost
import instance_allocator
import pprint


def pretty_result(result):
    pp = pprint.PrettyPrinter(depth=4)
    return pp.pprint(result)


def get_costs(n_cpu=None, n_hours=1, max_price=None):
    region_dict = read_cost('cost_file.json')
    if n_cpu is not None:
        if max_price is not None:
            print("CPU + Max prize combo")
            result = instance_allocator.instances_for_given_cpu_and_price(region_dict, n_hours, n_cpu, max_price)
        else:
            print("CPU + H hours combo")
            result = instance_allocator.instances_for_given_cpu_count(region_dict, n_hours, n_cpu)
    elif max_price is not None:
        print("Max price + H hours combo")
        result = instance_allocator.instances_for_given_price(region_dict, n_hours, max_price)
    else:
        print("Invalid input combo")
        result = [{'ERROR': 'Invalid input combination'}]
    pretty_result(result)


if __name__ == '__main__':
    # # The user requests for N CPUs for H hours
    # get_costs(n_cpu=115, n_hours=6)
    #
    # # The user requests for H hours with a maximum price
    # get_costs(n_hours=5, max_price=40)
    #
    # # The user requests for N CPUs for H hours with a maximum price
    # get_costs(n_cpu=100, n_hours=5, max_price=50)

    import argparse

    my_parser = argparse.ArgumentParser(description='Simple instance allocator')
    my_parser.add_argument('-cpu', type=int, required=False, help="The number of CPUs requested")
    my_parser.add_argument('-hours', type=int, required=True, help="The number of hours the CPU is requested for")
    my_parser.add_argument('-price', type=float, required=False, help="The max price the user can provide")
    args = my_parser.parse_args()

    get_costs(n_cpu=args.cpu, n_hours=args.hours, max_price=args.price)
