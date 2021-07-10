from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('login', login, name="login"),
    path('register', register, name="register"),
    path('logout/', logout, name = 'logout'),
]