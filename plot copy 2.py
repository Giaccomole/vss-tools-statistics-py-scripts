import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

data = pd.read_csv('vss_metadata.csv')
data_expanded = pd.read_csv('vss-expanded.csv')


# Plot A: Pure branches and instance branches
pure_branches = data[data['instances'] == '[]']['fqn'].count()
instance_branches = data[data['instances'] != '[]'].dropna(subset=['instances'])['fqn'].count()

fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(['Regular Branches', 'Instance Branches'], [pure_branches, instance_branches], color=['#5688c7', '#5b1865'])
for i, v in enumerate([pure_branches, instance_branches]):
    ax.text(i, v + 0.5, str(v), ha='center', fontsize=12)
ax.set_xlabel('Branch Type')
ax.set_ylabel('Count')
ax.set_title('Regular Branches vs Instantiatable Branches')

plt.tight_layout()
plt.show()

# Plot B: Sensor, Actuator, and Attribute counts next to branches
type_counts = Counter(data['type'])
branch_count = type_counts['branch']
sensor_count = type_counts['sensor']
actuator_count = type_counts['actuator']
attribute_count = type_counts['attribute']

fig, ax = plt.subplots(figsize=(8, 6))
x = ['Branches', 'Sensors', 'Actuators', 'Attributes']
y = [branch_count, sensor_count, actuator_count, attribute_count]
colors = ['#5688c7', '#5b1865', '#470024', '#251101']
ax.bar(x, y, color=colors)

for i, v in enumerate(y):
    ax.text(i, v + 0.5, str(v), ha='center', fontsize=12)

ax.set_xlabel('Type')
ax.set_ylabel('Count')
ax.set_title('Counts of Different Types')
plt.tight_layout()
plt.show()

# Plot A: Sensor, Actuator, and Attribute counts next to branches
type_counts = Counter(data_expanded['Type'])
branch_count = type_counts['branch']
sensor_count = type_counts['sensor']
actuator_count = type_counts['actuator']
attribute_count = type_counts['attribute']

fig, ax = plt.subplots(figsize=(8, 6))
x = ['Branches', 'Sensors', 'Actuators', 'Attributes']
y = [branch_count, sensor_count, actuator_count, attribute_count]
colors = ['#5688c7', '#5b1865', '#470024', '#251101']
ax.bar(x, y, color=colors)

for i, v in enumerate(y):
    ax.text(i, v + 0.5, str(v), ha='center', fontsize=12)

ax.set_xlabel('Type')
ax.set_ylabel('Count')
ax.set_title('Expanded Counts of Different Types')
plt.tight_layout()
plt.show()

def plot_expanded_types(data1, data2):
    """
    Plot the count of each type in a stacked bar chart with the original data on top.

    :param data1: The original data.
    :param data2: The expanded data.
    """
    type_counts1 = Counter(data1['type'])
    type_counts2 = Counter(data2['Type'])

    branch_count1 = type_counts1['branch']
    sensor_count1 = type_counts1['sensor']
    actuator_count1 = type_counts1['actuator']
    attribute_count1 = type_counts1['attribute']

    branch_count2 = type_counts2['branch']
    sensor_count2 = type_counts2['sensor']
    actuator_count2 = type_counts2['actuator']
    attribute_count2 = type_counts2['attribute']

    fig, ax = plt.subplots(figsize=(8, 6))

    x = ['Branches', 'Sensors', 'Actuators', 'Attributes']
    y1 = [branch_count1, sensor_count1, actuator_count1, attribute_count1]
    y2 = [branch_count2, sensor_count2, actuator_count2, attribute_count2]

    ax.bar(x, y1, color='#5688c7', label='Original')
    ax.bar(x, [y2[i] - y1[i] for i in range(len(y2))], bottom=y1, color='#5b1865', label='Expanded')

    for i, (v1, v2) in enumerate(zip(y1, y2)):
        ax.text(i, v1 + 0.5, str(int(v1)), ha='center', fontsize=12)
        ax.text(i, v2 + 0.5, str(int(v2)), ha='center', fontsize=12)

    ax.set_xlabel('Type')
    ax.set_ylabel('Count')
    ax.set_title('Counts of Different Types (Original Data on Top)')
    plt.tight_layout()
    plt.show()
    # Load the expanded CSV data
# Call the new plot function
plot_expanded_types(data, data_expanded)

