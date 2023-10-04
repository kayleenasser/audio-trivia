import constants

# get a list of just the paths
def extract_data_from_json(data, desired_key, current_data='', values=[]):
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{current_data}.{key}" if current_data else key
            extract_data_from_json(value, desired_key, new_path, values)
    elif isinstance(data, list):
        for item in data:
            extract_data_from_json(item, desired_key, current_data, values)
    elif current_data.endswith(desired_key):
        values.append(data)