import json
from django.http import HttpResponse
import environ
from django.shortcuts import render
import requests
env = environ.Env()

def safe_int(value, default=0):
    try:
        return int(value)
    except ValueError:
        return default

def home(request):
    env = environ.Env()
    trending_start = safe_int(request.GET.get('trending_start', 0))
    trending_limit = safe_int(request.GET.get('trending_limit', 6))
    all_start = safe_int(request.GET.get('all_start', 0))
    all_limit = safe_int(request.GET.get('all_limit', 10))

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': env('COINMARKETCAP_API_KEY')
    }
    trending_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/trending/latest'
    all_crypto_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    global_metrics_url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'
    
   
    trending_parameters = {
        'start': str(int(trending_start) + 1),
        'limit': str(trending_limit),
        'convert': 'USD'
    }
    all_crypto_parameters = {
        'start': str(int(all_start) + 1),
        'limit': str(all_limit),
        'convert': 'USD'
    }

    global_metrics_parameters = {
        'convert': 'USD'
    }


    try:
        trending_response = requests.get(trending_url, headers=headers, params=trending_parameters)
        trending_response.raise_for_status() 
        trending_data = trending_response.json()

        all_crypto_response = requests.get(all_crypto_url, headers=headers, params=all_crypto_parameters)
        all_crypto_response.raise_for_status()
        all_crypto_data = all_crypto_response.json()

        global_metrics_response = requests.get(global_metrics_url, headers=headers, params=global_metrics_parameters)

    except requests.RequestException as e:
        return HttpResponse('Failed to retrieve data: ' + str(e), status=500)

    except ValueError:
        return HttpResponse('Failed to parse JSON response', status=500)

    return render(request, 'home.html', {
        'trending': trending_data.get('data', []),
        'all_crypto': all_crypto_data.get('data', []),
        'trending_start': trending_start,
        'trending_limit': trending_limit,
        'all_start': all_start,
        'all_limit': all_limit,
        'global_metrics': global_metrics_response.json().get('data', {})
    })

# login, logout, register

def login(request):
    return render(request, 'login.html', name='login')

def logout(request):
    return render(request, 'logout.html', name='logout')

def register(request):
    return render(request, 'register.html', name='register')
