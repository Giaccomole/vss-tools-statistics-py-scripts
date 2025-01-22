import re
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data_expanded = pd.read_csv('vss-expanded.csv')
data_metadata = pd.read_csv('vss_metadata.csv')

# Convert IsInstance to boolean if necessary
data_expanded['IsInstance'] = data_expanded['IsInstance'].astype(bool)

# Identify instantiable branches in `vss-metadata.csv`
instantiable_branches = data_metadata[data_metadata['instances'] != '[]']
expanded_counts = {}
print("Debug: Inspecting instantiable branches...")

import re

def calculate_instance_count(instance_str):
    # Evaluate the string to get the list representation
    instance_list = eval(instance_str)
    count = 1
    for item in instance_list:
        if isinstance(item, list):
            # If the item is a sublist, multiply by the number of elements
            count *= len(item)
        elif isinstance(item, str):
            # Check if the string contains a range pattern
            # Check if the string contains a range pattern
            range_match = re.search(r'\[(\d+),(\d+)\]', item)
            if range_match:
                # If a range pattern is found, calculate the count for the range
                start, end = map(int, range_match.groups())
                count *= (end - start + 1)
            else:
                # If it's a single string, count it as one instance
                # Since it's already in a list, we don't need to do anything
                count = 2
    return count

for _, row in instantiable_branches.iterrows():
    fqn = row['fqn']  # Full hierarchical path
    base_name = fqn.split('.')[-1]  # Extract the base name
    instances = row['instances']  # Check the instances column in vss-metadata

    # Skip branches that do not have valid instances (empty list or NaN)
    if not isinstance(instances, str) or instances.strip() == '[]':

        continue

    print(f"Processing FQN: {fqn}, Base Name: {base_name}, Instances: {instances}")

    # Use the new function to calculate the number of instances
    instance_counts = calculate_instance_count(instances)

    expanded_counts[base_name] = instance_counts
    print(f"Count for {base_name}: {instance_counts}")

# If no matches were found, print a warning
if all(value == 0 for value in expanded_counts.values()):
    print("Warning: No expanded instances were found!")

# Preparing data for the stacked bar chart
expanded_names = list(expanded_counts.keys())
expanded_values = list(expanded_counts.values())

#


# Plotting Bar B
fig, ax = plt.subplots(figsize=(8, 10))

# Bar B: Stacked expanded instances
bottom = 0
for name, count in zip(expanded_names, expanded_values):
    if count > 0:  # Only plot non-zero bars
        ax.bar('Expanded Instances', count, bottom=bottom, label=name)
        

        ax.text('Expanded Instances', bottom + count / 2, f'{name}: {count}', ha='center', fontsize=10, color='white')
        bottom += count

# Adding total counts above the bar
total_expanded = sum(expanded_values)
ax.text('Expanded Instances', bottom + 10, f'Total: {total_expanded}', ha='center', fontsize=12, color='black')

# Labels, title, and legend
ax.set_xlabel('Category')
ax.set_ylabel('Count')
ax.set_title('Counts of Expanded Instances')
ax.legend(loc='upper left', fontsize=10)

plt.tight_layout()
plt.show()

