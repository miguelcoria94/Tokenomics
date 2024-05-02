from django.shortcuts import render
import requests
import environ

env = environ.Env()
def home(request):
    # Convert start and limit parameters safely to integers
    try:
        start = int(request.GET.get('start', 0))
        limit = int(request.GET.get('limit', 6))
    except ValueError:
        start = 0
        limit = 6  # Default values if conversion fails

# trending/gainers-losers endpoint
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/trending/latest'
    all_crypto = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    parameters = {
        'start': str(start + 1),  # API expects 1-based index
        'limit': str(limit),
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': env('COINMARKETCAP_API_KEY')
    }



    response = requests.get(url, headers=headers, params=parameters)
    all_crypto = requests.get(all_crypto, headers=headers, params=parameters)
    data = response.json()
    all_crypto = all_crypto.json()

    return render(request, 'home.html', {
        'trending': data['data'],
        'all_crypto': all_crypto['data'],
        'start': start,
        'limit': limit
    })
