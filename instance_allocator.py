from cost_file_reader import read_cost

instances_cpu_dict = {"large": 1, "xlarge": 2, "2xlarge": 4, "4xlarge": 8, "8xlarge": 16, "10xlarge": 32}

# per_region_result = {"region": "", "total_cost": "", "servers": []}
servers_list = []


def instances_for_given_hour(region_dict, hours, max_price):
    """

    :param region_dict:
    :param hours:
    :param max_price:
    :return: The number of servers for each region and their total costs

    We can find the number of servers required for an hour. The same number of servers would be used for the
    remaining hours too. Only their usage cost would be updated accordingly
    """
    result = []

    # hours and max price must be greater than zero
    if hours <= 0 or max_price <= 0:
        result.append({"ERROR": "Price and/or cost must be greater than zero"})
        return result

    # Calculate the number of servers for each region
    regions = region_dict.keys()

    for region in regions:
        server_count_dict = {}
        per_region_result = {"region": "", "total_cost": "", "servers": []}
        instances_cost_dict = region_dict[region]
        instances_list = list(instances_cost_dict.keys())

        # Initialising the count of each instances to zero
        for each_instance in instances_list:
            server_count_dict[each_instance] = 0

        total_price = 0
        # I can considering the max price for hour and allocate instances.
        max_price_for_one_hour = max_price / hours

        instance_index = 0

        while max_price_for_one_hour >= 0:
            current_instance = instances_list[instance_index]

            # If the instance can be considered, I update the price and max price is decreased
            cost_for_current_instance = instances_cost_dict[current_instance]
            if cost_for_current_instance <= max_price_for_one_hour:

                total_price = total_price + cost_for_current_instance

                max_price_for_one_hour = max_price_for_one_hour - cost_for_current_instance

                # The server count is incremented as it can be considered
                server_count_dict[current_instance] = server_count_dict[current_instance] + 1
            # If no instance can be bought for the available price, it means the above condition failed for the
            # smallest instance type
            elif instance_index == 0:
                break

            # we increment the index in a round robin method
            instance_index = (instance_index + 1) % len(instances_list)

        # result is updated. Since we have considered price only for one hour, we update it for total hours

        per_region_result["region"] = region
        per_region_result["total_cost"] = '$'+str(total_price * hours)
        for server, count in server_count_dict.items():
            if count > 0:
                per_region_result["servers"].append((server, count))

        result.append(per_region_result)

    # Result is sorted based on total cost
    result = sorted(result, key=lambda x: x['total_cost'])
    return result


if __name__ == '__main__':
    region_dict_input = read_cost('./cost_file.json')
    print(instances_for_given_hour(region_dict_input, 3, 29))
