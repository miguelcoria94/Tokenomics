from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth import login


urlpatterns = [
    path('', views.home, name='home'),
    path('crypto/<int:crypto_id>/', views.get_single_crypto, name='single_crypto'),
    path('login/', auth_views.LoginView.as_view(template_name='your_login_template.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
]