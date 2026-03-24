from django.urls import path
from . views import *


app_name = 'api'


urlpatterns = [

                # FEATURED HOUSES
        path('featured_houses', featured_houses, name='featured_houses'),

                # HOUSE DETAIL
        path('house_detail/<hid>/', house_detail, name='house_detail'),

                # FEATURED APARTMENTS
        path('featured_apartments', featured_apartments, name='featured_apartments'),

                # APARTMENT DETAILS
        path('apartment_detail/<apt_id>/', apartment_detail, name='apartment_detail'),

                # CATEGORY LIST
        path('category_list', category_list, name='category_list'),

                # CATEGORY DETAIL
        path('category_detail/<slug>/', category_detail, name='category_detail'),
    
    ]
