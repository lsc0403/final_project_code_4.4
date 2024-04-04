import pandas as pd

def transform_reviews_data(file_path):
    # load the data
    data = pd.read_excel(file_path)

    # transform the data
    data['Up Vote Cat'] = ['High' if x > data['Up Vote'].median() else 'Low' for x in data['Up Vote']]
    data['Total Vote Cat'] = ['High' if x > data['Total Vote'].median() else 'Low' for x in data['Total Vote']]
    data['Rating Cat'] = pd.cut(data['Rating'], bins=[0, 3, 6, 10], labels=['Low', 'Medium', 'High'], right=True)
    data['Probability Cat'] = ['High' if x >= 0.55 else 'Low' for x in data['Probability']]
    # data['Predicted Class Cat'] = ['Positive' if x == 1 else 'Negative' for x in data['Predicted Class']]
    data['Predicted Class Cat'] = ['Positive' if x == 0 else 'Neutral' if x == 1 else 'Negative' if x == 2 else 'Wrong'
                                   for x in data['Predicted Class']]

    # Select the transformed column
    transformed_data = data[['Movie Name', 'Title', 'Author', 'Date', 'Review',
                             'Up Vote Cat', 'Total Vote Cat', 'Rating Cat',
                             'Probability Cat', 'Predicted Class Cat']]

    # Save to a new Excel file.
    output_file_path = 'Excel_File/CThree-Transformed_IMDB_Reviews.xlsx'
    transformed_data.to_excel(output_file_path, index=False)

    print(f'Transformed data saved to {output_file_path}')

# Begin the transformation
file_path = 'Excel_File/BThree-Modified_IMDB_Reviews.xlsx'
transform_reviews_data(file_path)
