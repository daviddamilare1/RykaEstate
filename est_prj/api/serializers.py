from rest_framework import serializers
from core.models import *




















        # HOUSE SERIALIZERS
class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = [
            'name',
            'address',
            'image',
            'bedrooms',
            'bathrooms',
            'garage',
            'state',
            'city',
            'price',
            'sq_ft',
            'acres',
            'hid',
        ]


class HouseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = [
            'agent',
            'name',
            'desc',
            'address',
            'image',
            'bedrooms',
            'bathrooms',
            'garage',
            'state',
            'city',
            'price',
            'sq_ft',
            'acres',
            'year_build',
            'neigbourhood_info',
            
        ]
##############################################################################



        # APARTMENT SERIALIZERS
class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = [
            'name',
            'address',
            'image',
            'bedrooms',
            'bathrooms',
            'garage',
            'state',
            'city',
            'price',
            'sq_ft',
            'acres',
            'apt_id',
           
        ]





class ApartmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = [
            'agent',
            'name',
            'desc',
            'address',
            'image',
            'bedrooms',
            'bathrooms',
            'garage',
            'state',
            'city',
            'price',
            'year_build',
            'neigbourhood_info',
            
        ]
###########################################################################

        # CATEGORY SERIALIZERS
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = [
            'id', 'title', 'image', 'slug', 
        ]



class CategoryDetailSerializer(serializers.ModelSerializer):
    houses = HouseSerializer(many=True, read_only=True)
    apartments = ApartmentSerializer(many=True, read_only=True)
    class Meta:
        model = Categories
        fields = [
            'id', 'title', 'image', 'slug', 'houses', 'apartments'
        ]

#######################################################################

        # BOOKINGS SERIALIZERS
class BookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'user',
            'payment_status',
            'payment_method',
            'full_name',
            'phone',
            'email',
            'apartment',
            'total',
            'check_in_date',
            'check_out_date',
            'total_days',
            'checked_in',
            'checked_out',
            'is_active',
            'checked_in_tracker',
            'checked_out_tracker',
            'date',
            'booking_id',
            'success_id',
            'stripe_payment_intent'
        ]



# clas






