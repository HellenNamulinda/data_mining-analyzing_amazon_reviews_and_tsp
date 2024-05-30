import json
import os
import hashlib
import matplotlib.pyplot as plt
import numpy as np

# Define the directory containing the JSON files
root = os.path.dirname(os.path.abspath(__file__))
files_directory = os.path.abspath(os.path.join(root, '..', 'data'))

output_file = os.path.abspath(os.path.join(root, '..', 'Amazon_All_Categories.jsonl'))
duplicates_file = os.path.abspath(os.path.join(root, '..', 'Amazon_Duplicates.jsonl'))  # File for duplicates

# Initialize total record count
total_records = 0
total_records_before = 0
total_duplicates = 0  # Counter for duplicates

# Initialize set to store unique hashes of review JSON objects
unique_hashes = set()

# Initialize dictionaries to store category-specific record counts
category_records_before_dict = {}
category_records_after_dict = {}
category_duplicates_dict = {}

# Open the output file for writing
with open(output_file, 'w') as merged_file, open(duplicates_file, 'w') as duplicates:
    # Iterate over all json files in the directory
    for filename in os.listdir(files_directory):
        if filename.endswith('.jsonl'):
            category = os.path.splitext(filename)[0]  # Use filename (without extension) as category
            file_path = os.path.join(files_directory, filename)

            # Initialize category-specific record counts
            category_records_before = 0
            category_records_after = 0
            category_duplicates = 0  # Counter for duplicates in the current category

            with open(file_path, 'r') as file:
                # Read each line as a JSON object
                for line in file:
                    category_records_before += 1
                    total_records_before += 1

                    data = json.loads(line.strip())

                    # Hash the entire review JSON object
                    data_hash = hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()

                    # Check if the hash already exists, if so, write to duplicates file
                    if data_hash in unique_hashes:
                        # Add the category to the JSON object before writing to duplicates file
                        data['product_category'] = category
                        duplicates.write(json.dumps(data) + '\n')
                        total_duplicates += 1
                        category_duplicates += 1
                        continue

                    # Add the hash to the set
                    unique_hashes.add(data_hash)

                    # Add the category to the JSON object
                    data['product_category'] = category
                    # Write the modified JSON object to the output file
                    merged_file.write(json.dumps(data) + '\n')
                    category_records_after += 1
                    total_records += 1

            # Store category-specific record counts in dictionaries
            category_records_before_dict[category] = category_records_before
            category_records_after_dict[category] = category_records_after
            category_duplicates_dict[category] = category_duplicates

            print(f"Category '{category}' - Reviews before: {category_records_before}, after removing duplicates: {category_records_after}, duplicates: {category_duplicates}")

# Plotting grouped column chart for unique reviews in each category
categories = list(category_records_before_dict.keys())
before_values = list(category_records_before_dict.values())
after_values = list(category_records_after_dict.values())

x = np.arange(len(categories))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(14, 8))
bars1 = ax.bar(x - width/2, before_values, width, label='Before Removing Duplicates', color='blue')
bars2 = ax.bar(x + width/2, after_values, width, label='After Removing Duplicates', color='orange')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Product Category')
ax.set_ylabel('Number of Reviews')
ax.set_title('Number of Reviews Before and After Removing Duplicates in Each Category')
ax.set_xticks(x)
ax.set_xticklabels(categories, rotation=45, ha='right')
ax.legend()

# Adding labels to the bars
for bar in bars1:
    height = bar.get_height()
    ax.annotate('{}'.format(height),
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom',rotation=45)

for bar in bars2:
    height = bar.get_height()
    ax.annotate('{}'.format(height),
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom', rotation=45)

fig.tight_layout()

plt.savefig(os.path.abspath(os.path.join(root, '..', 'records_in_dataset.png')))
plt.close()

print(f"Files merged successfully into {output_file}")
print(f"Total reviews before removing duplicates: {total_records_before}")
print(f"Total reviews after removing duplicates: {total_records}")
print(f"Total duplicates saved to {duplicates_file}: {total_duplicates}")
