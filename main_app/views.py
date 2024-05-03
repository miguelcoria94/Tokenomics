import json
from django.http import HttpResponse
import environ
from django.shortcuts import render, redirect
import requests

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

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

def get_single_crypto(request, crypto_id):
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': env('COINMARKETCAP_API_KEY')
    }
    url = f'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
    parameters = {
        'id': crypto_id
    }

    chart_url = f'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/historical'
    chart_parameters = {
        'id': crypto_id
    }



    try:
        response = requests.get(url, headers=headers, params=parameters)
        response.raise_for_status()
        chart_response = requests.get(chart_url, headers=headers, params=chart_parameters)
        chart_response.raise_for_status()
        
        data = response.json()
        chart_data = chart_response.json()

        chart_data_json = json.dumps(chart_data['data']['quotes'])
        return render(request, 'single_crypto.html', {
        'crypto': data['data'][str(crypto_id)], 'chart_data': chart_data_json
    })

    except requests.RequestException as e:
        return HttpResponse('Failed to retrieve data: ' + str(e), status=500)

    except ValueError:
        return HttpResponse('Failed to parse JSON response', status=500)

    

# login, logout, register

def login(request):
    return render(request, 'login.html', name='login')

def logout(request):
    return render(request, 'logout.html', name='logout')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/accounts/login/')
        else:
            error_message = 'Invalid signup - try again'
    else:
        form = UserCreationForm()

    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)