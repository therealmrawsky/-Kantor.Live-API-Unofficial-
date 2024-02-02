
# Kantor.Live API (Unofficial)

Kantor.Live API is a Flask web application that scrapes exchange rates from the [Kantor.Live](https://kantor.live) website and provides an unofficial API endpoint to retrieve the data. The application also includes functionality to generate Google Maps links based on the kantor addresses.

## Getting Started

### Prerequisites

- Python (version 3.6 or higher)
- Flask
- Requests
- BeautifulSoup4
- Unidecode

You can install the required dependencies by running:

`pip install -r requirements.txt `

  ## Usage

Clone the repository:

`git clone https://github.com/your-username/exchange-rate-scraper.git
cd exchange-rate-scraper `

### Install dependencies:

`pip install -r requirements.txt`

  ### Run the Flask application:

`python main.py`
The application will start on http://localhost:9909/.
### API Endpoint

GET /get_exchange_rates: Retrieves exchange rates. 
### Optional query parameters:
	-city: The city for which you want to retrieve exchange rates.
	-opened: Set to 'yes' to include opened kantors. Default is 'no'.

## Example:

`curl http://localhost:9909/get_exchange_rates?city=gdansk&opened=yes `

Note: The base URL is 'https://kantor.live/kantory/' by default. To modify the base URL update the script accordingly.
Feel free to contribute to this project by opening issues or submitting pull requests.
## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/therealmrawsky/Kantor.Live-API-Unofficial/blob/main/LICENSE) file for details.
