from django.urls import path
from . import views

# <a
#     href="/?start={{ start + 6 }}&limit={{ limit }}"
#     class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
#     >Next 6</a
#   >

urlpatterns = [
    path('', views.home, name='home'),
]
