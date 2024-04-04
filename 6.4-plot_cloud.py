import json
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os


# Define function to read data
def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)


# Generate word clouds and save as images
def generate_wordclouds(data, output_dir):
    for movie, reviews in data.items():
        # Summarize all review texts and remove specific words
        # all_reviews = " ".join([review["Review"].replace("film", "").replace("movie", "").replace("one", "") for review in reviews])
        all_reviews = " ".join(
            [str(review["Review"]).replace("film", "").replace("movie", "").replace("one", "") for review in reviews])

        # Create a word cloud object
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_reviews)
        # Save the word cloud image
        output_path = os.path.join(output_dir, f"{movie}_wordcloud.png")
        wordcloud.to_file(output_path)


# Generate HTML file to display the word clouds

def generate_html(data, output_dir,output_total):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Movie Reviews Wordclouds</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f8f9fa;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .title {
                text-align: center;
                margin-bottom: 20px;
                font-size: 24px;
            }
            .btn {
                display: block;
                width: 100%;
                padding: 10px;
                margin-bottom: 10px;
                font-size: 16px;
                background-color: #007bff;
                color: #fff;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            .btn:hover {
                background-color: #0056b3;
            }
            .wordcloud-img {
                display: none;
                max-width: 100%;
                height: auto;
                margin-top: 10px;
                border-radius: 5px;
                box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
            }
        </style>
        <script>
        function showWordcloud(movie) {
            var image = document.getElementById(movie);
            if (image.style.display === 'none') {
                image.style.display = 'block';
            } else {
                image.style.display = 'none';
            }
        }
        </script>
    </head>
    <body>
    <div class="container">
        <h2 class="title">Word Clouds</h2>
    """
    for movie, _ in data.items():
        # Handle quotes in movie names
        movie_formatted = movie.replace("'", "\\'")
        image_path = f"{output_dir}/{movie}_wordcloud.png"  # Use relative path
        html_content += f"<button class='btn' onclick='showWordcloud(\"{movie_formatted}\")'>{movie}</button>"
        html_content += f"<img id='{movie_formatted}' class='wordcloud-img' src='{image_path}'>"
    html_content += """
            </div>
            </body>
            </html>
            """

    with open("Page_and_JSON/6.4-plot_cloud.html", "w") as html_file:  # Output to the same folder as the code
        html_file.write(html_content)


if __name__ == "__main__":
    filepath = 'Page_and_JSON/BThree-JSONData.json'  # Update to actual file path
    output_dir = 'wordcloud_images'  # Folder for outputting word cloud images
    output_dir2 = 'Page_and_JSON'
    output_total = os.path.join(output_dir2, output_dir)
    os.makedirs(output_total, exist_ok=True)

    data = load_data(filepath)
    generate_wordclouds(data, output_total)
    generate_html(data, output_dir,output_total)
