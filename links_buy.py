from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from unique_scraper_buy import scrape_apartment_details
from selenium.webdriver.support import expected_conditions as EC
import time

def main1(city_url, canton):
    driver = webdriver.Chrome()


    try:
        driver.get(city_url)

        all_apartment_urls = []
        count = 0

        while True:
            time.sleep(2)  # Adjust this sleep duration as needed

            apartment_links = driver.find_elements(By.CSS_SELECTOR, 'a[id^="link-result-item-"][category="Vente"]')
            for link in apartment_links:
                href = link.get_attribute("href")
                all_apartment_urls.append(href)
                print(href)

            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.next'))
                )
                next_button.click()
                count += 1
                print("Navigating to next page")
            except (NoSuchElementException, TimeoutException):
                print("Collected all apartment URLs.")
                break

        for url in all_apartment_urls:
            scrape_apartment_details(url, canton)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()





