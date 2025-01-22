import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the data
data = pd.read_csv('vss_metadata.csv')

# Count the types
type_counts = Counter(data['type'])
counts = {
    'Branches': type_counts.get('branch', 0),
    'Sensors': type_counts.get('sensor', 0),
    'Actuators': type_counts.get('actuator', 0),
    'Attributes': type_counts.get('attribute', 0),
}

# Sort by descending order
sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=False)
x = [item[0] for item in sorted_counts]
y = [item[1] for item in sorted_counts]

# Save the counts to a CSV file
counts_df = pd.DataFrame(sorted_counts, columns=['Type', 'Count'])
counts_df.to_csv('type_counts.csv', index=False)

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
colors = ['#5688c7', '#5b1865', '#470024', '#251101']

# Horizontal bar chart
bars = ax.barh(x, y, color=colors)

# Add inscriptions inside the bars
for bar, value in zip(bars, y):
    ax.text(value - 5, bar.get_y() + bar.get_height() / 2,  # Adjust position slightly inside
            str(value), va='center', ha='right', color='white', fontsize=12)

# Labels and title
ax.set_xlabel('Count')
ax.set_ylabel('Type')
ax.set_title('Counts of Different Types in VSS')
plt.tight_layout()
plt.show()
