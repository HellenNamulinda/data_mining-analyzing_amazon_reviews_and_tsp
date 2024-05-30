import pandas as pd
import matplotlib.pyplot as plt
import json
import os


# Function to load data from a text file into a DataFrame
def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            asin_category = eval(parts[0])
            review_data = json.loads(parts[1])
            data.append({
                'product_id': asin_category[0],
                'category': asin_category[1],
                'total_reviews': review_data['total_reviews'],
                'positive_reviews': review_data['sentiment_counts']['positive'],
                'neutral_reviews': review_data['sentiment_counts']['neutral'],
                'negative_reviews': review_data['sentiment_counts']['negative']
            })
    return pd.DataFrame(data)


# Load the data
root = os.path.dirname(os.path.abspath(__file__))
file_path_reviews = os.path.abspath(os.path.join(root, '../..', 'outputs', 'amazon_sentiment_analysis_output.txt'))
reviews_df = load_data(file_path_reviews)

# Get top 10 products based on total reviews
top_10_products = reviews_df.sort_values(by='total_reviews', ascending=False).head(10)

# Combine product ID and category for x-axis labels
top_10_products['label'] = top_10_products['product_id'] + ' (' + top_10_products['category'] + ')'

# Summary statistics of reviews for top 10 products
reviews_summary = top_10_products.groupby('label')[
    ['total_reviews', 'positive_reviews', 'neutral_reviews', 'negative_reviews']].sum()

# Column plot of sentiment counts by category for top 10 products
ax = reviews_summary.plot(kind='bar', figsize=(15, 10))
plt.title('Sentiment Counts by Category for Top 10 Most Reviewed Products', pad=20)
plt.xlabel('Product (Category)')
plt.ylabel('Number of Reviews')
plt.xticks(rotation=45)
plt.legend(title='Sentiment', labels=['Total', 'Positive', 'Neutral', 'Negative'])
plt.tight_layout()

# Adding data labels to the bars
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 5), textcoords='offset points', rotation=45)

plt.savefig(os.path.abspath(os.path.join(root, '../..', 'outputs/visualizations', 'sentiment_counts_by_category.png')))
plt.close()