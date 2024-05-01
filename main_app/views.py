from django.shortcuts import render
import requests
import environ

env = environ.Env()
def home(request):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '6',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': env('COINMARKETCAP_API_KEY')
    }

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    
    return render(request, 'home.html', {'cryptos': data['data']})