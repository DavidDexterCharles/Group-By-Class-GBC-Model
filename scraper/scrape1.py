import requests
from bs4 import BeautifulSoup

# Function to scrape and process each page
def scrape_page(url):
    # Fetch the HTML content of the page
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all the article links on the page
        article_links = soup.find_all('a', class_='col-sm-9')
        for link in article_links:
            article_url = link['href']
            article_title = link.text.strip()
            print("Title:", article_title)
            print("URL:", article_url)
            # Access the content of each article if needed
            # article_response = requests.get(article_url)
            # article_content = article_response.text
            # Process the content as needed
            print()
    else:
        print("Failed to fetch page:", url)

# Base URL of the CDC website
base_url = "https://archive.cdc.gov"
# URL pattern for listing pages
listing_url = "https://archive.cdc.gov/#/results?q=%20health%20emergencies&start={}&rows=10"

# Iterate over multiple pages
for page_number in range(0, 100, 10):  # Adjust range as needed
    current_listing_url = listing_url.format(page_number)
    print("Scraping page:", current_listing_url)
    scrape_page(current_listing_url)
