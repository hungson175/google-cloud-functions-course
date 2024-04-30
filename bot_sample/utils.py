import datetime
import json


# convert ms to datetime
def ms_to_datetime(ms):
    return datetime.datetime.fromtimestamp(ms / 1000.0)

# beautify json output
def beautify_json(json_data):
    print(json.dumps(json_data, indent=4))



# Print the schema of a dictionary, assumed that if there is a list, all elements are of the same type
def print_dict_schema(data, indent=0):
    for key, value in data.items():
        # Print the key and the type of its value
        print(' ' * indent + f"{key}: {type(value).__name__}", end='')

        # Check if the value is a dictionary
        if isinstance(value, dict):
            print()  # Move to the next line before diving into the nested dictionary
            print_dict_schema(value, indent + 4)
        # Check if the value is a list
        elif isinstance(value, list):
            if value:
                # Check if the first item in the list is a dictionary
                if isinstance(value[0], dict):
                    print(" of dictionaries containing:")
                    print_dict_schema(value[0], indent + 4)
                else:
                    # Print the type of the first item, assuming all items are the same type
                    print(f" of {type(value[0]).__name__} elements")
            else:
                # If the list is empty, print a generic message
                print(" of elements of unknown type")
        else:
            print()  # Move to the next line after printing the type

# Get the schema of a dictionary, assumed that if there is a list, all elements are of the same type
def get_dict_schema(data):
    schema = {}
    for key, value in data.items():
        if isinstance(value, dict):
            schema[key] = get_dict_schema(value)
        elif isinstance(value, list):
            if value:
                if isinstance(value[0], dict):
                    # Assume all items in the list are dictionaries of the same structure
                    schema[key] = [get_dict_schema(value[0])]
                else:
                    # List of simple types
                    schema[key] = [type(value[0]).__name__]
            else:
                schema[key] = ['UnknownType']
        else:
            schema[key] = type(value).__name__
    return schema

# print the assets with walletBalance > 0
def print_account_assets(account):
    for asset in account['assets']:
        if float(asset['walletBalance']) > 0:
            print(f"{asset['asset']} : {asset['walletBalance']}")