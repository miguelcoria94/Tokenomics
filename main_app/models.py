from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse

class Cryptocurrency(models.Model):
    crypto_id = models.IntegerField(unique=True)

    def __str__(self):
        return f'Crypto ID: {self.crypto_id}'

class Watchlist(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    cryptos = models.ManyToManyField(Cryptocurrency)

    def __str__(self):
        crypto_ids = ', '.join(str(crypto.crypto_id) for crypto in self.cryptos.all())
        return f'{self.user.username} - {crypto_ids}'
