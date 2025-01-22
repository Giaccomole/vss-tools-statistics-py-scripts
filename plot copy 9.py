import pandas as pd
import itertools

# Load the data into a DataFrame
data_metadata = pd.read_csv('vss_metadata.csv')

# Extract the substring between the first and second delimiter "."
data_metadata['components'] = data_metadata['fqn'].apply(lambda x: x.split('.')[1] if len(x.split('.')) > 1 else '')
data_metadata['property'] = data_metadata['type'].apply(
    lambda x: "dynamic" if x in ["sensor", "actuator"] else "static"
)

# Get the list of remaining column names
column_names = data_metadata.columns.tolist()

# Swap the first and second column names
column_names[0], column_names[1] = column_names[1], column_names[0]

# Swap the 12th and 13th column names
column_names[11], column_names[12] = column_names[12], column_names[11]

# # Swap the 12th and 13th column names
# column_names[11], column_names[2] = column_names[2], column_names[11]

# Reorder the data columns
data_metadata = data_metadata[column_names]
# Drop the specified columns
columns_to_drop = [1, 2, 3, 4, 6, 7, 8, 9, 10,11,12]
data_metadata.drop(data_metadata.columns[columns_to_drop], axis=1, inplace=True)

data_metadata['value'] = 0


# Function to print unique values in each column
def print_unique_values(data):
    for column in data.columns:
        unique_values = data[column].unique()
        print(f"Unique values in column '{column}':")
        print(unique_values)
        print("-" * 50)

columns = list(data_metadata.columns)
columns[0], columns[2] = columns[2], columns[0]  # Swap the positions of column 0 and column 2
data_metadata = data_metadata[columns]

columns = list(data_metadata.columns)
columns[1], columns[2] = columns[2], columns[1]  # Swap the positions of column 0 and column 2
data_metadata = data_metadata[columns]

# Call the function
print_unique_values(data_metadata)

data_metadata = data_metadata[~data_metadata.isin(['branch']).any(axis=1)]
# Save the modified data into a new CSV file
data_metadata.to_csv('modified_vss_compact_metadata.csv', index=False)

# Generate all possible combinations of unique values
unique_values = [data_metadata[column].unique() for column in data_metadata.columns]
combinations = list(itertools.product(*unique_values))

# Create a new DataFrame with all possible combinations
combinations_df = pd.DataFrame(combinations, columns=data_metadata.columns)

# Count the occurrences of each combination in the original DataFrame
counts = data_metadata.groupby(list(data_metadata.columns)).size().reset_index(name='count')


# Merge the combinations DataFrame with the counts
combinations_counts_df = pd.merge(combinations_df, counts, on=list(data_metadata.columns), how='left').fillna(0)

# Ensure the counts are integers
combinations_counts_df['count'] = combinations_counts_df['count'].astype(int)
# Save the combinations and counts to a new CSV file
combinations_counts_df.to_csv('combinations_counts_vss_metadata.csv', index=False)

print(combinations_counts_df)
