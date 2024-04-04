import pandas as pd

# Read Excel file
df = pd.read_excel('Excel_File/positive_for_use.xlsx')

# Group according to 'Movie Name' and keep only the first 600 rows in each group
result_df = df.groupby('Movie Name').head(600)

# Write the processed data back to a new Excel file
result_df.to_excel('Excel/filtered_test.xlsx', index=False)


