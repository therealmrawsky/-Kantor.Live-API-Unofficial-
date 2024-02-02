from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from unidecode import unidecode

app = Flask(__name__)

def scrape_exchange_rates(url):
    # Fetch exchange rates from the provided URL
    response = requests.get(url)

    if response.status_code == 200:
        # Parse HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        exchange_rate_elements = soup.find_all('tr', class_='d-flex flex-column d-md-table-row w-100 card-wrapper card-simple')
        exchange_rates = {}

        for exchange_rate_element in exchange_rate_elements:
            # Extract information for each exchange rate entry
            kantor_name = exchange_rate_element.find('a', class_='kantor-name').text.strip()
            currency_elements = exchange_rate_element.find_all('div', class_='grid-item-currency')
            rates_elements = exchange_rate_element.find_all('div', class_='grid-item')

            # Handle cases where rates are present
            if rates_elements:
                rates_elements = [element for element in rates_elements if 'grid-item-currency' not in element.get('class', [])]

            currency_rates = {}
            kantor_address_div = exchange_rate_element.find('div', class_='d-md-flex flex-row align-items-start')
            address_pattern = re.compile(r'\b\w{2}\.\s*\w+\s*\w+\s*\d+(?:/\d+)?|\w+\s*\d+\b')
            matches = address_pattern.findall(kantor_address_div.text)
            kantor_address = matches[0] if matches else None
            kantor_address = kantor_address.strip() if kantor_address else None

            # Extract currency rates for each currency in the entry
            for i in range(len(currency_elements)):
                currency = currency_elements[i].text.strip()
                buy_rate = rates_elements[i * 2].text.strip()
                sell_rate = rates_elements[i * 2 + 1].text.strip()
                currency_rates[currency] = {'buy': buy_rate, 'sell': sell_rate}

            exchange_rates[kantor_name] = {'address': kantor_address, 'currencies': currency_rates}

        return exchange_rates

    else:
        # Print an error message if fetching fails
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return None

def scrape_all_pages(base_url, num_pages, opened):
    # Scrape exchange rates from all pages
    all_exchange_rates = {}
    pagination_sign = '&' if opened else '?'

    for page in range(1, num_pages + 1):
        url = f"{base_url}{pagination_sign}page={page}"
        exchange_rates = scrape_exchange_rates(url)

        if exchange_rates:
            all_exchange_rates.update(exchange_rates)

    return all_exchange_rates

def generate_google_maps_link(city, address):
    # Generate a Google Maps link with encoded city and address
    address_encoded = quote(address, safe='')
    return f'https://www.google.com/maps/search/{city}+{address_encoded}'

@app.route('/get_exchange_rates', methods=['GET'])
def get_exchange_rates():
    # Set default number of pages and base URL
    num_pages = 2
    base_url = 'https://kantor.live/kantory/'  # Update the base URL

    # Extract city and opened parameters from the query string
    city = request.args.get('city')
    opened = request.args.get('opened')

    # Convert non-ASCII characters in the city to ASCII equivalents
    if city:
        city = unidecode(city)

    # Modify the base URL based on the provided city and opened parameters
    if city:
        base_url += f'{city}/'
    if opened:
        base_url += f"?opened=yes"
    all_exchange_rates = scrape_all_pages(base_url, num_pages, opened)

    if all_exchange_rates:
        # Add Google Maps link to each exchange rate entry
        for kantor_name, exchange_rate_info in all_exchange_rates.items():
            address = exchange_rate_info.get('address')
            if address:
                google_maps_link = generate_google_maps_link(city, address)
                exchange_rate_info['google_maps_link'] = google_maps_link

        return jsonify(all_exchange_rates)
    else:
        return jsonify({'error': 'Failed to fetch exchange rates.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=9909)
