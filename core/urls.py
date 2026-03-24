from django.urls import path
from . views import *


app_name = 'core'


urlpatterns = [
        # INDEX 
    path('', index, name='index'),

        # HOUSES
    path('houses', houses, name='houses'),

        # APARTMENTS
    path('apartments', apartments, name='apartments'),

        # FILTER PROPERTIES
    path('filter_properties', filter_properties, name='filter_properties'),

        # HOUSE DETAILS
    path('house_details/<hid>/<agent_id>/', house_details, name='house_details'),

        # APARTMENT DETAILS
    path('apt_details/<apt_id>/<agent_id>/', apt_details, name='apt_details'),

        # ADD COMMENT
    path('add_comment/<apt_id>/', add_comment, name='add_comment'),

        # CHECK APARTMENT AVAILABILITY
    path('check_apartment_availability/', check_apartment_availability, name='check_apartment_availability'),

        # CHECKOUT PAGE
    path('payment_page/<booking_id>/', payment_page, name='payment_page'),

        # API CHECKOUT SESSION
    path('api/create_checkout_session/<booking_id>/', create_checkout_session, name='api_create_checkout_session'),
    
        # PAYMENT SUCCESS
    path('payment_success/<booking_id>/', payment_success, name='payment_success'),

           # Payent Failed  
    path('payment_failed/<booking_id>/', payement_failed , name="payment_failed"),

            # UPDATE APARTMENT STATUS
    path('update_apartment_status/', update_apartment_status, name='update_apartment_status'),
    
    
    
    ]
