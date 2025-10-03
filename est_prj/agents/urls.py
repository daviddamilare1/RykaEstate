from django.urls import path
from . views import *


app_name = 'agent'


urlpatterns = [
        # AGENTS LIST
    path('agents', agents, name='agents'),
        # AGENT DETAILS 
    path('agent_details/<agent_id>/', agent_details, name='agent_details'),

        # ADD COMMENT
    path('add_comment/<agent_id>/', add_comment, name='add_comment'),

        # DASBOARD
    path('dashboard', dashboard, name='dashboard'),

        # AGENT APARTMENT LISTINGS
    path('agent_apartments', agent_apartments, name='agent_apartments'),

        # CREATE APARTMENT
    path('create_apartment', create_apartment, name='create_apartment'),

        # EDIT APARTMENT
    path('edit_apartment/<apt_id>/', edit_apartment, name='edit_apartment'),

        # DELETE APARTMENT
    path('delete_apartment/<apt_id>/', delete_apartment, name='delete_apartment'),

        # AGENT HOUSES
    path('agent_houses', agent_houses, name='agent_houses'),

        # CREATE HOUSE
    path('create_house', create_house, name='create_house'),

        # EDIT HOUSE
    path('edit_house/<hid>/', edit_house, name='edit_house'),

        # DELETE APARTMENT
    path('delete_house/<hid>/', delete_house, name='delete_house'),

        # BOOKINGS
    path('bookings', bookings, name='bookings'),

        # BOOKING DETAILS
    path('booking_details/<booking_id>/', booking_details, name='booking_details'),

        # NOTIFICATIONS
    path('notifications', notifications, name='notifications'),
    
        # CLOSE NOTIFICATION
    path('close_notification/', close_notification, name='close_notification'),

        # CREATE AGENT
    path('create_agent', create_agent, name='create_agent'),

        # EDIT AGENT DETAILS
    path('edit_agent_details', edit_agent_details, name='edit_agent_details'),
    
    ]