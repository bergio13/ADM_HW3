import nltk
import re
import requests
from bs4 import BeautifulSoup

# Function to preprocess the text
def preprocess_text(description):
    # Convert to lowercase
    description = description.lower()
    
    # Tokenize
    tokens = nltk.word_tokenize(description)
    
    # Remove stopwords and punctuation
    stop_words = nltk.corpus.stopwords.words('english')
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

    # Stemming
    stemmer = nltk.PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]

    # Join tokens back into a string
    processed_text = ' '.join(tokens)

    return processed_text

# Define a function to extract the fees and currency
def preprocess_fees(fees, exchange_rates):
    # Create a dictionary to store the fees and currency
    fdf = {'fees': 0, 'currency': ''}
    
    # Check if the fees is a string
    if isinstance(fees, str):
        # Remove commas and dots and replace the currency names with the corresponding symbol
        fees = fees.replace(',', '').replace('.', '')
        fees = fees.replace('EUR', '€').replace('GBP', '£').replace('Eur', '€').replace('Euro', '€').replace('euros', '€')

        # Extract the fees and currency using regular expressions
        fees_values = re.findall(r'£\s?(\d+)', fees)
        fees_values2 = re.findall(r'€\s?(\d+)', fees)
        fees_values3 = re.findall(r'\$\s?(\d+)', fees)
        fees_values4 = re.findall(r'(\d+)\sSEK', fees)
        fees_values5 = re.findall(r'([0-9]+)\s?€', fees)
        
        # Store the fees and currency in the dictionary
        if fees_values:
            fdf['fees'] = int(max(fees_values))
            fdf['currency'] = '£'
        elif fees_values2:
            fdf['fees'] = int(max(fees_values2))
            fdf['currency'] = '€'
        elif fees_values3:
            fdf['fees'] = int(max(fees_values3))
            fdf['currency'] = '$'
        elif fees_values4:
            fdf['fees'] = int(max(fees_values4))
            fdf['currency'] = 'SEK'
        elif fees_values5:
            fdf['fees'] = int(max(fees_values5))
            fdf['currency'] = '€'
        
        if fdf['fees']: 
            fdf['fees'] = round(fdf['fees'] * exchange_rates.get(fdf['currency'], 1), 2)
    
    return fdf['fees'], fdf['currency']

# Define a function to get the exchange rates from the European Central Bank
def get_exchange_rates():
    # Define url of the page to scrape
    url = 'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html'
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract EUR/USD, EUR/GBP and EUR/SEK exchange rates
        exchange_rate_eur_usd = soup.find_all('span', class_='rate')[0].text
        exchange_rate_eur_gbp = soup.find_all('span', class_='rate')[5].text
        exchange_rate_eur_sek = soup.find_all('span', class_='rate')[9].text

    # Compute GBP/USD exchange rate
    exchange_rate_gbp_usd = float(exchange_rate_eur_usd) / float(exchange_rate_eur_gbp)
    # Define a dictionary to store the exchange rates
    exchange_rates = {'$': 1, '€': float(exchange_rate_eur_usd), '£':exchange_rate_gbp_usd, 'SEK': float(exchange_rate_eur_sek)}
    
    return exchange_rates
