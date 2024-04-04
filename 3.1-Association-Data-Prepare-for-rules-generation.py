import pandas as pd

def transform_reviews_data(file_path):
    # Load the data
    data = pd.read_excel(file_path)
    # Calculate the average length of reviews
    average_length = data['Review'].apply(lambda x: len(x.split())).mean()

    # Define thresholds for review length categories
    short_threshold = average_length * 0.5  # Reviews with less than 50% of the average length
    long_threshold = average_length * 1.5  # Reviews with more than 150% of the average length

    # Categorize review lengths
    data['Review Cat'] = data['Review'].apply(lambda x: 'long' if len(x.split()) > long_threshold
    else 'medium' if len(x.split()) > short_threshold
    else 'short')
    # Transform the data high&low&medium
    up_vote_high_threshold = data['Up Vote'].quantile(0.33)
    up_vote_low_threshold = data['Up Vote'].quantile(0.67)

    total_vote_high_threshold = data['Total Vote'].quantile(0.33)
    total_vote_low_threshold = data['Total Vote'].quantile(0.67)

    # Assign 'High', 'Medium', 'Low' to each column based on these thresholds
    data['Up Vote Cat'] = ['High' if x <= up_vote_high_threshold else 'Low' if x >= up_vote_low_threshold else 'Medium'
                           for x in data['Up Vote']]
    data['Total Vote Cat'] = [
        'High' if x <= total_vote_high_threshold else 'Low' if x >= total_vote_low_threshold else 'Medium' for x in
        data['Total Vote']]

    data['Rating Cat'] = pd.cut(data['Rating'], bins=[0, 3, 6, 10], labels=['Low', 'Medium', 'High'], right=True)
    # Select the transformed column
    transformed_data = data[['Movie Name', 'Title', 'Author', 'Date', 'Review Cat',
                             'Up Vote Cat', 'Total Vote Cat', 'Rating Cat',
                             'Predicted Class Cat']]

    # Save to a new Excel file.
    output_file_path = 'Excel_File/K-means_ready_for_generation.xlsx'
    transformed_data.to_excel(output_file_path, index=False)

    print(f'Transformed data saved to {output_file_path}')

# Begin the transformation
file_path = 'Excel_File/K-means_rules_dataset.xlsx'
transform_reviews_data(file_path)
