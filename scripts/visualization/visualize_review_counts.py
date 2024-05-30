import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Function to load data from a text file into a DataFrame
def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            asin_category = eval(parts[0])
            value = int(parts[1])
            data.append({
                'product_id': asin_category[0],
                'category': asin_category[1],
                'review_counts': value
            })
    return pd.DataFrame(data)

# Load the number of reviews data
root = os.path.dirname(os.path.abspath(__file__))
file_path_reviews = os.path.abspath(os.path.join(root, '../..', 'outputs', 'amazon_count_reviews_output.txt'))
reviews_df = load_data(file_path_reviews)

# Summary statistics of number of reviews
reviews_summary = reviews_df.groupby('category')['review_counts'].describe()

# Count of products per category based on reviews
category_counts_reviews = reviews_df['category'].value_counts()

# Set up the matplotlib figure for reviews
plt.figure(figsize=(14, 8))

# Bar plot of the count of products per category based on reviews
plt.figure(figsize=(15, 10))
ax_reviews = category_counts_reviews.plot(kind='bar')
plt.title('Number of Products by Category (Reviews)', pad=20)
plt.xlabel('Category')
plt.ylabel('Number of Products')
plt.xticks(rotation=45)

# Add the count labels on top of each bar
for p in ax_reviews.patches:
    ax_reviews.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005), rotation=45)

plt.tight_layout()
plt.savefig(os.path.abspath(os.path.join(root, '../..', 'outputs/visualizations', 'number_of_products_by_category.png')))
plt.close()

# Histogram of average ratings
plt.figure(figsize=(15, 10))
sns.histplot(reviews_df['review_counts'], bins=50)
plt.title('Distribution of Reviews Counts')
plt.xlabel('Review Counts')
plt.ylabel('Number of Products')
plt.yscale('log')  # Set y-axis scale to logarithmic
plt.savefig(os.path.abspath(os.path.join(root, '../..', 'outputs/visualizations', 'reviews_counts_distribution.png')))
plt.close()
