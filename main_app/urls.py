from django.urls import path
from . import views

# <a
#     href="/?start={{ start + 6 }}&limit={{ limit }}"
#     class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
#     >Next 6</a
#   >

# login, logout, register

urlpatterns = [
    path('', views.home, name='home'),
    path('crypto/<int:crypto_id>/', views.get_single_crypto, name='single_crypto'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    

]
