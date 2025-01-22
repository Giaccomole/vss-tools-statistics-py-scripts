import csv
import json

def read_csv(filename):
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        return list(csv_reader)

def add_to_tree(tree, path, leaf_value=1, leaf_type=None):
    parts = path.split('.')
    if parts[0] == 'Vehicle':
        parts = parts[1:]  # Skip the first keyword if it's 'Vehicle'
    
    current = tree
    
    for part in parts:
        found = False
        for child in current['children']:
            if child['name'] == part:
                current = child
                found = True
                break
        
        if not found:
            new_node = {'name': part, 'children': []}
            current['children'].append(new_node)
            current = new_node
    
    # Add leaf-specific properties (value and type)
    current['value'] = leaf_value
    if leaf_type:  # Add the `type` property only if provided
        current['type'] = leaf_type

def generate_json_from_csv(csv_data):
    result = {
        "name": "Vehicle",
        "type": "Node",
        "children": [
            {
                "name": "Branches",
                "type": "Node",
                "children": []
            },
            {
                "name": "Properties",
                "type": "Node",
                "children": [
                    {"name": "Static Properties (Attributes)","type": "Node", "children": []},
                    {
                        "name": "Changing Properties",
                        "type": "Node",
                        "children": [
                            {"name": "Sensors", "type": "Node","children": []},
                            {"name": "Actuators","type": "Node","children": []}
                        ]
                    }
                ]
            }
        ]
    }

    for row in csv_data:
        fqn = row['fqn']
        type_ = row['type']
        
        if type_ == 'branch':
                add_to_tree(result['children'][0], fqn)
        elif type_ == 'attribute':
            add_to_tree(result['children'][1]['children'][0], fqn, leaf_type='attribute')
        elif type_ == 'sensor':
            add_to_tree(result['children'][1]['children'][1]['children'][0], fqn, leaf_type='sensor')
        elif type_ == 'actuator':
            add_to_tree(result['children'][1]['children'][1]['children'][1], fqn, leaf_type='actuator')

    return result

if __name__ == "__main__":
    csv_data = read_csv('vss_metadata.csv')
    json_result = generate_json_from_csv(csv_data)
    
    print(json.dumps(json_result, indent=2))
    
    # Save the new JSON data to a file
    with open('newdata2.json', 'w') as file:
        json.dump(json_result, file, indent=2)
