import pandas as pd
import json

# Load the data
data_metadata = pd.read_csv('vss_metadata.csv')

# Identify instantiable branches in `vss_metadata.csv`
instantiable_branches = data_metadata[data_metadata['instances'].notnull() & (data_metadata['instances'] != '[]')]

# Function to create a tree structure from FQN
def add_to_tree(tree, fqn, instances):
    parts = fqn.split('.')
    current_level = tree
    for part in parts:
        # Check if the part already exists in the current level
        found = False
        for child in current_level['children']:
            if child['name'] == part:
                current_level = child
                found = True
                break
        if not found:
            new_node = {"name": part, "children": []}
            current_level['children'].append(new_node)
            current_level = new_node

    # Add instances as children
    for instance in instances:
        current_level['children'].append({"name": instance, "value": 0})  # Replace 0 with actual value if available

# Create the root of the tree
root = {"name": "Instance Branches", "children": []}

# Populate the tree with instantiable branches
for _, branch in instantiable_branches.iterrows():
    fqn = branch['fqn']
    instances_str = branch['instances']
    try:
        instances = eval(instances_str) if isinstance(instances_str, str) else []
    except:
        instances = []
    add_to_tree(root, fqn, instances)

# Convert the tree to JSON format
tree_json = json.dumps(root, indent=2)

# Print the JSON
print(tree_json)

# Optionally, save the JSON to a file
with open('tree_structure.json', 'w') as f:
    f.write(tree_json)