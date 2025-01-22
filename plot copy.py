import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

# Load the CSV data
data = pd.read_csv('vss-expanded.csv')

# Plot A: Sensor, Actuator, and Attribute counts next to branches
type_counts = Counter(data['Type'])
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
