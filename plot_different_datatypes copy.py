import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the data
data = pd.read_csv('vss_metadata.csv')

# Count the types
type_counts = Counter(data['datatype'])
counts = {
    'int8': type_counts.get('int8', 0),
    'int16': type_counts.get('int16', 0),
    'int32': type_counts.get('int32', 0),
    'uint8': type_counts.get('uint8', 0),
    'uint16': type_counts.get('uint16', 0),
    'uint32': type_counts.get('uint32', 0),
    'string': type_counts.get('string', 0),
    'boolean': type_counts.get('boolean', 0),
    'float': type_counts.get('float', 0),
    'double': type_counts.get('double', 0)
}


# Sort by descending order
sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=False)
x = [item[0] for item in sorted_counts]
y = [item[1] for item in sorted_counts]

# Save the counts to a CSV file
counts_df = pd.DataFrame(sorted_counts, columns=['Datatype', 'Count'])
counts_df.to_csv('datatype_counts.csv', index=False)

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
colors = ['#5688c7', '#5a7aa4', '#5a6d81', '#59605e', '#4f4c3b', '#472118', '#470024', '#251101']


# Horizontal bar chart
bars = ax.barh(x, y, color=colors)

# Add inscriptions inside the bars
for bar, value in zip(bars, y):
    ax.text(value - 5, bar.get_y() + bar.get_height() / 2,  # Adjust position slightly inside
            str(value), va='center', ha='right', color='white', fontsize=12)

# Labels and title
ax.set_xlabel('Count')
ax.set_ylabel('Datatype')
ax.set_title('Counts of Different Datatypes in VSS')
plt.tight_layout()
plt.show()
