import pandas as pd

# File paths for input and output
input_file_path = "/Users/kartikmittal/Desktop/LLM Challenges/all_posts_data_raw.csv"
output_file_path = "/Users/kartikmittal/Desktop/LLM Challenges/all_posts_data_title.csv"

# Read the CSV file
df = pd.read_csv(input_file_path)

# Clean the URLs in the Post_Link column to extract the titles
df['Title'] = df['Post_Link'].str.replace('https://community.openai.com/t/', '', regex=True)
df['Title'] = df['Title'].str.replace('/\d+', '', regex=True)  # Remove numbers at the end of the URL
df['Title'] = df['Title'].str.replace('-', ' ')  # Replace all "-" with spaces to format the title

# Save the result to a new CSV file
df.to_csv(output_file_path, index=False)

print("Titles extracted successfully!")
