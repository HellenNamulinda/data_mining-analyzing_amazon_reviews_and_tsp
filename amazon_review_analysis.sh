#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

#echo "$SCRIPT_DIR"

# Merge Datasets
echo "Merging datasets for downloaded categories"
python3 "$SCRIPT_DIR"/scripts/merge_datasets.py

# Define the dataset
input_file=("$SCRIPT_DIR/Amazon_All_Categories.jsonl")

mkdir -p "$SCRIPT_DIR/"outputs
# Define Python scripts for all the Jobs
python_scripts=("amazon_count_reviews.py" "amazon_product_average_rating.py" "amazon_top_reviewed_products.py" "amazon_average_helpfulness_score.py" "amazon_sentiment_analysis.py")

# Loop Over All Jobs
for script in "${python_scripts[@]}"; do
    # Print the script being executed
    echo "Executing script: $script"
    # Execute each job and pass the input file as argument
    python3 "$SCRIPT_DIR/scripts/$script" "${input_file[@]}" > "$SCRIPT_DIR/outputs/${script%.py}_output.txt"
done

# Final Visualizations
echo "Generating visualizations for the  Review Counts"
python3 "$SCRIPT_DIR"/scripts/visualization/visualize_review_counts.py

echo "Generating visualizations for the  Average Ratings"
python3 "$SCRIPT_DIR"/scripts/visualization/visualize_average_ratings.py

echo "Generating visualizations for the  Average Helpfulness Scores"
python3 "$SCRIPT_DIR"/scripts/visualization/visualize_average_helpfulness_scores.py

echo "Generating visualizations for the  Sentiments"
python3 "$SCRIPT_DIR"/scripts/visualization/visualize_sentiments.py
