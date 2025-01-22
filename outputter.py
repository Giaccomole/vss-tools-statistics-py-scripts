import json

# Load the input JSON data
with open('VVVehicleSignalSpecification.json', 'r') as file:
    data = json.load(file)



# Define a function to recursively build the new JSON structure
def build_json_structure(obj, parent_name=None):
    result = []
    for key, value in obj.items():
        item = {'name': key}
        if 'children' in value:
            item['children'] = build_json_structure(value['children'], key)
        else:
            for prop, prop_value in value.items():
                if prop != 'children':
                    item[prop] = prop_value
        result.append(item)
    return result

# Build the new JSON structure
new_data = {
    'name': 'Vehicle',
    'type': 'Vehicle',
    'children': build_json_structure(data['Vehicle']['children'])
}

# Save the new JSON data to a file
with open('output.json', 'w') as file:
    json.dump(new_data, file, indent=2)