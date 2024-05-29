import json
import threading

# Import the scraping functions from your modules
from links_buy import main1 as scrape_buy
from links_rent import main2 as scrape_rent

def scrape_canton(canton, scrape_function):
    canton_name = canton['name']
    url_key = 'buy' if scrape_function == scrape_buy else 'rent'
    url = canton.get(url_key)
    if url:
        print(f"Starting '{url_key}' scrape for {canton_name}")
        scrape_function(url, canton_name)
        print(f"Finished '{url_key}' scrape for {canton_name}")

def main():
    # Load JSON data from file
    with open('canton_urls.json', 'r') as file:
        data = json.load(file)

    # Prepare to process cantons with threading
    for i in range(0, len(data['cantons']), 6):  # Process 6 cantons at a time
        threads = []

        # Iterate through 6 cantons and create threads for 'buy' and 'rent'
        for canton in data['cantons'][i:i+6]:
            if 'buy' in canton and canton['buy']:
                buy_thread = threading.Thread(target=scrape_canton, args=(canton, scrape_buy))
                threads.append(buy_thread)
                buy_thread.start()

            if 'rent' in canton and canton['rent']:
                rent_thread = threading.Thread(target=scrape_canton, args=(canton, scrape_rent))
                threads.append(rent_thread)
                rent_thread.start()

        # Wait for all threads in this batch to complete
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    main()
