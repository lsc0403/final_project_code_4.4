import pandas as pd

# Load data
data = pd.read_excel('Excel_File/BThree-Modified_IMDB_Reviews.xlsx')

# Calculate the median for Up Vote and Total Vote
up_vote_median = data['Up Vote'].median()
total_vote_median = data['Total Vote'].median()
average_length = data['Review'].apply(lambda x: len(str(x).split())).mean()
data['Review Length'] = data['Review'].apply(lambda x: len(str(x).split()))

up_vote_high_threshold = data['Up Vote'].quantile(0.33)
up_vote_low_threshold = data['Up Vote'].quantile(0.67)

total_vote_high_threshold = data['Total Vote'].quantile(0.33)
total_vote_low_threshold = data['Total Vote'].quantile(0.67)
# Define thresholds for review length categories
# For simplicity, you might consider "short" as below average, "medium" as around average,
# and "long" as above average. Adjust these definitions as needed.
short_threshold = average_length * 0.5  # Reviews with less than 50% of the average length
long_threshold = average_length * 1.5  # Reviews with more than 150% of the average length


# Copy the data for comparison
data_before = data.copy()

# Apply conditions to update the Predicted Class column
# cluster=6
data.loc[
    # (data['Probability'] < 0.676) &
    (data['Up Vote'] > up_vote_high_threshold) &
    (data['Total Vote'] > total_vote_high_threshold) &
    (data['Review Length'] < short_threshold) &
    (data['Rating'].between(7, 10, inclusive="both")), 'Predicted Class'] = 0
# cluster=4
data.loc[
    # (data['Probability'] < 0.650) &
    (data['Up Vote'] < up_vote_high_threshold) &
    (data['Total Vote'] < total_vote_high_threshold) &
    ((data['Review Length'] < long_threshold) & (data['Review Length'] > short_threshold)) &
    (data['Rating'].between(7, 10, inclusive="both")), 'Predicted Class'] = 0
# cluster=5
data.loc[
    # (data['Probability'] < 0.564) &
    (data['Up Vote'] < up_vote_low_threshold) &
    (data['Total Vote'] < total_vote_low_threshold) &
    ((data['Review Length'] < long_threshold) & (data['Review Length'] > short_threshold)) &
    (data['Rating'].between(0, 3, inclusive="both")), 'Predicted Class'] = 2
# cluster=8
data.loc[
    # (data['Probability'] < 0.585) &
    (data['Up Vote'] < up_vote_low_threshold) &
    (data['Total Vote'] < total_vote_low_threshold) &
    (data['Review Length'] < short_threshold) &
    (data['Rating'].between(0, 3, inclusive="both")), 'Predicted Class'] = 2
# Compare the Predicted Class column before and after the changes to identify modified rows
modified_rows = data[data['Predicted Class'] != data_before['Predicted Class']]

# Save the updated DataFrame
data.to_excel('Excel_File/DThree-Modified_IMDB_Reviews_Updated.xlsx', index=False)

# Print the modified rows
print("Modified rows:")
print(modified_rows)

