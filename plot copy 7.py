import json
import re

# Function to parse range strings like "Row[1,4]"
def parse_range(range_str):
    match = re.match(r'(\w+)\[(\d+),(\d+)\]', range_str)
    if match:
        base = match.group(1)
        start = int(match.group(2))
        end = int(match.group(3))
        return [f"{base}{i}" for i in range(start, end + 1)]
    return [range_str]

# Function to create combinations of instances
def create_combinations(ranges_and_lists):
    if not ranges_and_lists:
        return [[]]
    
    first, *rest = ranges_and_lists
    rest_combinations = create_combinations(rest)
    
    combinations = []
    for item in first:
        for combination in rest_combinations:
            combinations.append([item] + combination)
    
    return combinations

# Function to add to tree
def add_to_tree(tree, branch_name, instances):
    # Parse instances
    parsed_instances = []
    for instance in instances:
        if isinstance(instance, list):
            parsed_instances.append(instance)
        else:
            parsed_instances.append(parse_range(instance))
    
    # Create combinations only if there are multiple lists or ranges at the same level
    if len(parsed_instances) > 1:
        combinations = create_combinations(parsed_instances)
        combined_instances = ['.'.join(combination) for combination in combinations]
    else:
        combined_instances = [item for sublist in parsed_instances for item in sublist]
    
    # Add the branch as a child to the root
    branch_node = {"name": branch_name, "children": []}
    for instance in combined_instances:
        branch_node['children'].append({"name": instance, "value": 0})  # Replace 0 with actual value if available
    tree['children'].append(branch_node)

# Function to process JSON data
def process_json(data, parent_key=''):
    if 'children' in data:
        for key, value in data['children'].items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            if 'instances' in value:
                add_to_tree(root, new_key, value['instances'])
            process_json(value, new_key)

# Load the data from JSON file
with open('VVVehicleSignalSpecification.json', 'r') as f:
    data_metadata = json.load(f)

# Create the root of the tree
root = {"name": "Instance Branches", "children": []}

# Process the JSON data
process_json(data_metadata)

# Convert the tree to JSON format
tree_json = json.dumps(root, indent=2)

# Print the JSON
print(tree_json)

#
