from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

def scraper(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(), options=options)
    driver.get(url)
    time.sleep(2)

    output = []
    while True:
        # Wait for the "Load More" button to be clickable
        try:
            load_more_button = driver.find_element(By.CSS_SELECTOR, 'button.load-more-button')
            ActionChains(driver).move_to_element(load_more_button).click().perform()
            time.sleep(2)  # Adjust sleep time as necessary
        except:
            break  # Exit loop if no more "Load More" button

        # Scrape the newly loaded products
        product_cards = driver.find_elements(By.CSS_SELECTOR, 'div.ProductCard_content')

        for card in product_cards:
            try:
                title = card.find_element(By.CSS_SELECTOR, '[data-testid="product-card-title"]').text.strip()
            except:
                title = None

            try:
                price = card.find_element(By.CSS_SELECTOR, 'span[class*="PriceTag_actual"]').text.strip()
            except:
                price = None

            try:
                rating = card.find_element(By.CSS_SELECTOR, 'div._6zw1gna').text.strip()
            except:
                rating = None

            try:
                rating_count_elem = card.find_element(By.CSS_SELECTOR, 'div._6zw1gnb._6zw1gna')
                rating_count_text = rating_count_elem.text.strip()  # e.g., "(14)"
                rating_count = rating_count_text.strip("()")    # "14"
            except:
                rating_count = "0"

            output.append({
                'brand': title.split()[0] if title else None,
                'model': ' '.join(title.split()[1:]) if title else None,
                'title': title,
                'price': price,
                'rating': rating,
                'number_of_ratings': rating_count,
                'url': card.find_element(By.TAG_NAME, 'a').get_attribute('href')
            })

    driver.quit()
    return output

def remove_duplicates(products):
    seen = set()
    unique = []
    for p in products:
        key = p['url']
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique

collection_url = 'https://www.jbhifi.com.au/collections/headphones-speakers-audio/true-wireless-earbuds'
raw_data = scraper(collection_url)
clean_data = remove_duplicates(raw_data)

with open('jbhifi_tws_earbuds.json', 'w', encoding='utf-8') as f:
    json.dump(clean_data, f, indent=4, ensure_ascii=False)

print(f"✅ Scraped {len(clean_data)} unique products and saved to JSON.")
