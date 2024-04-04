import torch
import transformers
from torch import nn
import pandas as pd
import re
from html import unescape

# Define the Transformer model class
class Transformer(nn.Module):
    def __init__(self, transformer, output_dim, freeze=True):
        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.config.hidden_size
        self.fc = nn.Linear(hidden_dim, output_dim)
        if freeze:
            for param in self.transformer.parameters():
                param.requires_grad = False

    def forward(self, ids, attention_mask=None):
        output = self.transformer(ids, attention_mask=attention_mask)
        hidden = output.last_hidden_state
        cls_hidden = hidden[:, 0, :]
        prediction = self.fc(cls_hidden)
        return prediction

# Load the tokenizer and model
transformer_name = "bert-base-uncased"
tokenizer = transformers.AutoTokenizer.from_pretrained(transformer_name)
transformer_model = transformers.AutoModel.from_pretrained(transformer_name)

# Define the model, here setting the output dimension to 3
output_dim = 3  # There are 3 output categories: positive, neutral, negative
model = Transformer(transformer_model, output_dim, freeze=True)

# check the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Load the trained model weights
model.load_state_dict(torch.load("transformerThreeRecall_eachMovie.pt", map_location=device))
print("The model has been loaded successfully.")

# Define the prediction function
def predict_sentiment(text, model, tokenizer, device):
    model.eval()
    encoded_input = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding=True)
    ids = encoded_input['input_ids'].to(device)
    attention_mask = encoded_input['attention_mask'].to(device)
    with torch.no_grad():
        outputs = model(ids, attention_mask=attention_mask)
        predictions = torch.softmax(outputs, dim=1)
        predicted_class = torch.argmax(predictions, dim=1).item()
        predicted_probability = predictions[0][predicted_class].item()
    return predicted_class, predicted_probability

def clean_text(text):
    # HTML decode
    text = unescape(text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove email addresses
    text = re.sub(r'\S*@\S*\s?', '', text)
    # Replace numbers with a specific marker (or choose to remove them)
    text = re.sub(r'\d+', ' ', text)
    # Remove special symbols and punctuation (adjust as needed)
    text = re.sub(r'[^\w\s]', '', text)
    # Replace consecutive whitespace characters with a single space
    text = re.sub(r'\s+', ' ', text)
    # Remove whitespace characters at the beginning and end of the text
    text = text.strip()
    return text
# Set the file name
file_name = 'Excel_File/A-IMDB_Reviews.xlsx'
# Read the xls file
df = pd.read_excel(file_name)

# Determine the position of the 'Review' column
review_col_index = df.columns.get_loc("Review")
# Initialize a list to collect dictionaries
cleaned_data = []
# Insert new columns before the 'Review' column to store the prediction results and probabilities
df.insert(review_col_index, 'Probability', pd.NA)
df.insert(review_col_index, 'Predicted Class', pd.NA)

print("Begin review prediction")
count=0
# Iterate through the movie reviews to make predictions, and fill the new columns with the prediction results
for index, row in df.iterrows():
    count = count+1
    if count/1000 == 0:
        print(count)
    # text = row['Review']
    clean_review = clean_text(row['Review'])  # clean the text
    predicted_class, predicted_probability = predict_sentiment(clean_review, model, tokenizer, device)
    df.at[index, 'Predicted Class'] = predicted_class
    df.at[index, 'Probability'] = predicted_probability
    # Collect the data from the cleaned DataFrame
    cleaned_data.append(
        {'Cleaned Review': clean_review, 'Predicted Class': predicted_class, 'Probability': predicted_probability})

# Create a new DataFrame from the list of dictionaries
df_cleaned = pd.DataFrame(cleaned_data)
# Save the modified file
modified_file_name = 'Excel_File/BThree-Modified_IMDB_Reviews.xlsx'
df.to_excel(modified_file_name, index=False)
# Save a file that only includes the cleaned comments and prediction results
# Create a new DataFrame from the list of dictionaries
cleaned_file_name = 'Excel_File/B2Three-Cleaned_IMDB_Reviews_Predictions.xlsx'
df_cleaned.to_excel(cleaned_file_name, index=False)