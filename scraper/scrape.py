import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def extract_data_from_iframe(url):
    # # Fetch the HTML content of the URL
    # response = requests.get(url)
    # if response.status_code != 200:
    #     print("Failed to fetch the URL:", url)
    #     return None
    # # Parse the HTML content
    # soup = BeautifulSoup(response.content, 'html.parser')
    
    # Launch a headless browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # To run Chrome in headless mode
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(20)  # Adjust the wait time as needed
    soup = BeautifulSoup(driver.page_source, 'html.parser')


    # Find the iframe
    iframe = soup.find('iframe')
    if not iframe:
        print("No iframe found in the URL:", url)
        return None
    
    # Extract the source URL of the iframe
    iframe_src = iframe['src']
    
    # Fetch the HTML content of the iframe source URL
    iframe_response = requests.get(iframe_src)
    if iframe_response.status_code != 200:
        print("Failed to fetch the iframe source URL:", iframe_src)
        return None
    
    # Parse the HTML content of the iframe source URL
    iframe_soup = BeautifulSoup(iframe_response.content, 'html.parser')
    
    # Find all <p> tags and extract their text
    p_tags = iframe_soup.find_all('p')
    extracted_data = [p.get_text() for p in p_tags]
    
    return ' '.join(extracted_data)

# URL containing the iframe
# url = "https://archive.cdc.gov/#/details?q=health&start=90&rows=10&url=https://www.cdc.gov/niosh/twh/newsletter/twhnewsv5n2.html"
url="https://archive.cdc.gov/#/details?q=health&start=110&rows=10&url=https://www.cdc.gov/globalhealth/security/stories/cameroon-muscle-memory.html"
# Extract data from the iframe
data = extract_data_from_iframe(url)
if data:
    print(data)
    # for i, item in enumerate(data, 1):
    #     print(f"Paragraph {i}: {item}")
