import json


def read_cost(file_name):
    try:
        with open(file_name) as file:
            cost_data = json.load(file)
        return cost_data
    except FileNotFoundError:
        return {"ERROR": "File not found"}
    except ValueError:
        return {"ERROR": "Invalid input data"}


if __name__ == '__main__':
    print(read_cost('./cost_file.json'))
