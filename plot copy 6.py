import re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Load the data
data_expanded = pd.read_csv('vss-expanded.csv')
data_metadata = pd.read_csv('vss_metadata.csv')

# Convert IsInstance to boolean if necessary
data_expanded['IsInstance'] = data_expanded['IsInstance'].astype(bool)

# Identify instantiable branches in `vss-metadata.csv`
instantiable_branches = data_metadata[data_metadata['instances'] != '[]']
expanded_counts = {}

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
            range_match = re.search(r'\[(\d+),(\d+)\]', item)
            if range_match:
                start, end = map(int, range_match.groups())
                count *= (end - start + 1)
            else:
                count *= 1
    return count

for _, row in instantiable_branches.iterrows():
    fqn = row['fqn']  # Full hierarchical path
    base_name = fqn.split('.')[-1]  # Extract the base name
    instances = row['instances']

    if not isinstance(instances, str) or instances.strip() == '[]':
        continue

    instance_counts = calculate_instance_count(instances)
    expanded_counts[base_name] = instance_counts

# Export the expanded counts to a CSV file
expanded_counts_df = pd.DataFrame(list(expanded_counts.items()), columns=['Name', 'Count'])
expanded_counts_df.to_csv('expanded_counts.csv', index=False)

# Prepare data for the horizontal bar chart
sorted_expanded_counts = sorted(expanded_counts.items(), key=lambda x: x[1], reverse=False)
expanded_names = [name for name, count in sorted_expanded_counts]
expanded_values = [count for name, count in sorted_expanded_counts]

# Custom color palette
custom_palette = [
    "#251101", "#470024", "#5b1865", "#2c5784", "#5688c7",
    "#191970", "#003153", "#1560bd", "#0f52ba", "#007ba7",
    "#30d5c8", "#50c878", "#00a86b", "#228b22", "#6b8e23",
    "#cc7722", "#a0522d", "#8a3324", "#800000", "#8b668b"
]

# Plotting horizontal bar chart
fig, ax = plt.subplots(figsize=(12, 8))
colours = custom_palette[:len(expanded_names)]  # Ensure enough colors

# Horizontal bar chart
ax.barh(expanded_names, expanded_values, color=colours)

# Add counts above the bars
for i, count in enumerate(expanded_values):
    ax.text(count, i, str(count), va='center', ha='left', fontsize=10)

# Labels, title, and grid
ax.set_xlabel('Count')
ax.set_ylabel('Expanded Instances')
ax.set_title('Counts of Expanded Instances')
ax.grid(axis='x')

plt.tight_layout()
plt.show()
