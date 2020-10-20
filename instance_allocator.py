from cost_file_reader import read_cost

instances_cpu_dict = {"large": 1, "xlarge": 2, "2xlarge": 4, "4xlarge": 8, "8xlarge": 16, "10xlarge": 32}

result = []
# per_region_result = {"region": "", "total_cost": "", "servers": []}
servers_list = []


def instances_for_given_hour(hours, max_price):
    region_dict = read_cost('./cost_file.json')
    print(region_dict)
    regions = region_dict.keys()
    server_count_dict = {}
    for region in regions:
        server_count_dict = {}
        per_region_result = {"region": "", "total_cost": "", "servers": []}
        instances_cost_dict = region_dict[region]
        instances_list = list(instances_cost_dict.keys())

        # Initialising the count of each instances to zero
        for each_instance in instances_list:
            server_count_dict[each_instance] = 0

        price = 0
        # I can considering the max price for one hour
        max_price_for_one_hour = max_price / hours

        instance_index = 0

        while max_price_for_one_hour >= 0:
            current_instance = instances_list[instance_index]
            if instances_cost_dict[current_instance] <= max_price_for_one_hour:
                price = price + instances_cost_dict[current_instance]
                max_price_for_one_hour = max_price_for_one_hour - instances_cost_dict[current_instance]
                server_count_dict[current_instance] = server_count_dict[current_instance] + 1
            elif instance_index == 0:
                break
            instance_index = (instance_index + 1) % len(instances_list)

        per_region_result["region"] = region
        per_region_result["total_cost"] = price * hours
        for server, count in server_count_dict.items():
            if count > 0:
                per_region_result["servers"].append((server, count*hours))

        print(per_region_result)


if __name__ == '__main__':
    instances_for_given_hour(3, 10)
