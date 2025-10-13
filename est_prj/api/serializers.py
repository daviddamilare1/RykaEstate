from rest_framework import serializers
from core.models import *





















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




