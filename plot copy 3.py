import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

data = pd.read_csv('vss_metadata.csv')
data_expanded = pd.read_csv('vss-expanded.csv')

# Plot A: Stacked Bars for instance vs ordinary branches and Leaves
ordinary_branches = data[data['instances'] == '[]']['fqn'].count()
instance_branches = data[data['instances'] != '[]'].dropna(subset=['instances'])['fqn'].count()

# Type counts for sensors, actuators, attributes in the original data
type_counts = Counter(data['type'])
sensor_count = type_counts['sensor']
actuator_count = type_counts['actuator']
attribute_count = type_counts['attribute']

# First bar: Stack ordinary branches and instantiatable branches
fig, ax = plt.subplots(figsize=(8, 10))  # Make the plot taller (increase height)

# First bar: ordinary and instantiatable branches stacked
ax.bar('Branches', ordinary_branches, color='#5688c7', label='Ordinary Branches')
ax.bar('Branches', instance_branches, bottom=ordinary_branches, color='#5b1865', label='Instantiatable Branches')

# Second bar: stack Sensors, Actuators, and Attributes
ax.bar('Leaves', sensor_count, color='#470024', label='Sensors')
ax.bar('Leaves', actuator_count, bottom=sensor_count, color='#251101', label='Actuators')
ax.bar('Leaves', attribute_count, bottom=sensor_count + actuator_count, color='#2c5784', label='Attributes')

# Add annotations for each segment inside the bars and next to count numbers
ax.text('Branches', ordinary_branches / 2, f'{ordinary_branches} Ordinary Branches', ha='center', fontsize=12, color='white')
ax.text('Branches', ordinary_branches + instance_branches / 2, f'{instance_branches} Instantiatable Branches', ha='center', fontsize=12, color='white')

ax.text('Leaves', sensor_count / 2, f'{sensor_count} Sensors', ha='center', fontsize=12, color='white')
ax.text('Leaves', sensor_count + actuator_count / 2, f'{actuator_count} Actuators', ha='center', fontsize=12, color='white')
ax.text('Leaves', sensor_count + actuator_count + attribute_count / 2, f'{attribute_count} Attributes', ha='center', fontsize=12, color='white')

# Adding total heights on top of the bars
total_branches = ordinary_branches + instance_branches
total_leaves = sensor_count + actuator_count + attribute_count

# Place the total counts above the bars
ax.text('Branches', total_branches + 10, f'Total: {total_branches}', ha='center', fontsize=12, color='black')  # Adjust the vertical position slightly for visibility
ax.text('Leaves', total_leaves + 10, f'Total: {total_leaves}', ha='center', fontsize=12, color='black')  # Adjust the vertical position slightly for visibility


# Labels and title
ax.set_xlabel('Category')
ax.set_ylabel('Count')
ax.set_title('Stacked Counts for Branch Types and Leaf Categories')
ax.legend(loc='upper left')

plt.tight_layout()
plt.show()
