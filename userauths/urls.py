from django.urls import path
from . views import *




app_name = 'userauths'




urlpatterns = [

        # SIGN UP
    path('sign_up', sign_up, name='sign_up'),

        # SIGN IN
    path('sign_in', sign_in, name='sign_in'),

        # SIGN OUT
    path('sign_out', sign_out, name='sign_out'),
]
