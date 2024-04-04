import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans

# load the data
file_path = 'Excel_File/K-means_ready_for_generation.xlsx'
data = pd.read_excel(file_path)

# Initialize the label encoder
le_up_vote = LabelEncoder()
le_total_vote = LabelEncoder()
le_predicted_class = LabelEncoder()
le_review = LabelEncoder()

# Encode categorical variables
data['Up Vote Cat Encoded'] = le_up_vote.fit_transform(data['Up Vote Cat'])
data['Total Vote Cat Encoded'] = le_total_vote.fit_transform(data['Total Vote Cat'])
data['Predicted Class Cat Encoded'] = le_predicted_class.fit_transform(data['Predicted Class Cat'])
data['Review Cat Encoded'] = le_review.fit_transform(data['Review Cat'])
# Select features for clustering
features = data[['Up Vote Cat Encoded', 'Total Vote Cat Encoded', 'Review Cat Encoded']]

# Perform K-means clustering
kmeans = KMeans(n_clusters=8, random_state=42)
data['Cluster'] = kmeans.fit_predict(features)

# View clustering results
print(data[['Up Vote Cat', 'Total Vote Cat', 'Review Cat', 'Cluster']].head())
# Analyze the distribution within each cluster
for cluster in range(kmeans.n_clusters): # Assuming we have 4 clusters
    print(f"Cluster {cluster} distribution:")
    print(data[data['Cluster'] == cluster]['Predicted Class Cat'].value_counts())
    print("\n")
    print(f"Cluster {cluster} summary:")

    # Calculate and print the most frequent category for the original categorical features
    for column in ['Up Vote Cat', 'Total Vote Cat', 'Review Cat']:
        most_frequent = data[data['Cluster'] == cluster][column].mode()[0]
        print(f"Most frequent {column}: {most_frequent}")

    # Print the mean values of the encoded features
    for column in ['Up Vote Cat Encoded', 'Total Vote Cat Encoded', 'Review Cat Encoded']:
        mean_value = data[data['Cluster'] == cluster][column].mean()
        print(f"{column} mean: {mean_value}")

    print("\n")
