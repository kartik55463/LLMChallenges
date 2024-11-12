import requests
from bs4 import BeautifulSoup
import csv
import time

# Base URL for scraping the latest posts across the entire forum
base_url = "https://community.openai.com/latest?page={}&per_page=50"

all_data = []
page_number = 0

# Loop through pages until no more posts are found
while True:
    url = base_url.format(page_number)
    
    while True:
        try:
            resp = requests.get(url)
            resp.raise_for_status()  # Raise an error if the request fails
            break  # Break the loop when the request is successful
        except requests.exceptions.HTTPError as e:
            if resp.status_code == 429:
                print("Rate limited. Sleeping for 60 seconds.")
                time.sleep(60)  # Wait for 1 minute before retrying
            else:
                raise e

    page_content = resp.text

    # Use BeautifulSoup to parse the page content
    soup = BeautifulSoup(page_content, "html.parser")

    # Find all the posts on the page
    topic_items = soup.find_all("tr", class_="topic-list-item")

    # Break the loop if no posts are found on the page
    if not topic_items:
        print(f"No more posts found on page {page_number}. Stopping.")
        break

    # Extract data from each post
    for item in topic_items:
        # Extract the origination date
        date = item.find_all("td")[-1].text.strip()

        # Extract the number of views
        views = item.find("td", class_="views").text.strip()

        # Extract the number of replies
        replies = item.find("td", class_="replies").text.strip()

        # Extract the category name
        category_name = item.find("span", class_="category-name").text.strip()

        # Extract tags
        tag_links = item.find_all("a", class_="discourse-tag")
        tags = [link.text for link in tag_links]

        # Extract the post link
        post_link = item.find("a", class_='title')['href']

        # Create a dictionary to store the extracted data
        data_dict = {
            "Date": date,
            "Views": views,
            "Replies": replies,
            "Category": category_name,
            "Tags": ", ".join(tags),
            "Post_Link": post_link  # Add the link to the post
        }

        all_data.append(data_dict)

    # Log progress
    print(f"Scraped {len(topic_items)} posts from page {page_number}.")

    # Move to the next page
    page_number += 1

    # Add a longer delay to prevent rate limiting or blocking
    time.sleep(3)

# Specify the path and file name where the CSV file will be saved
csv_file_path = 'all_posts_data_raw.csv'

# Write the collected data to a CSV file
with open(csv_file_path, mode="w", newline='', encoding="utf-8") as f:
    csvwriter = csv.writer(f)

    # Write the header row
    csvwriter.writerow(["Date", "Views", "Replies", "Category", "Tags", "Post_Link"])

    # Write the data rows
    for data_dict in all_data:
        csvwriter.writerow(data_dict.values())

print(f"Scraping completed. {len(all_data)} posts saved to {csv_file_path}")
