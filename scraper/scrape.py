from selenium import webdriver
from bs4 import BeautifulSoup

url = "https://archive.cdc.gov/#/results?q=%20health%20emergencies&start=10&rows=10"

# Launch a headless browser
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # To run Chrome in headless mode
driver = webdriver.Chrome(options=options)

# Get the page content
driver.get(url)

# Wait for JavaScript to render the page
driver.implicitly_wait(10)  # Adjust the wait time as needed

# Now, you can parse the HTML content
soup = BeautifulSoup(driver.page_source, 'html.parser')
article_links = soup.find_all('a', class_='col-sm-9')

# Process the article links
for link in article_links:
    article_url = link['href']
    article_title = link.text.strip()
    print("Title:", article_title)
    print("URL:", article_url)
    print()

# Close the browser
driver.quit()
