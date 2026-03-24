from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response


from core.models import *
from .serializers import *










        # FEATURED HOUSES
@api_view(['GET'])
def featured_houses(request):
    featured_houses = House.objects.filter(featured=True, status='live', is_sold=False)
    serializer = HouseSerializer(featured_houses, many=True)
    return Response(serializer.data)




        # HOUSE DETAIL
@api_view(['GET'])
def house_detail(request, hid):
    house = House.objects.get(hid=hid, status='live', agent__verified=True)
    serializer = HouseDetailSerializer(house)
    return Response(serializer.data)









        # FEATURED APARTMENTS
@api_view(['GET'])
def featured_apartments(request):
    featured_apartments = Apartment.objects.filter(featured=True, is_available=True, agent__verified=True, status='live')
    serializer = ApartmentSerializer(featured_apartments, many=True)
    return Response(serializer.data)



        # APARTMENT DETAILS
@api_view(['GET'])
def apartment_detail(request, apt_id):
    apartment = Apartment.objects.get(apt_id=apt_id, status='live', agent__verified=True)
    serializer = ApartmentDetailSerializer(apartment)
    return Response(serializer.data)





@api_view(['GET'])
def category_list(request):
    categories = Categories.objects.all()
    serializer = CategoryListSerializer(categories, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def category_detail(request, slug):
    categories = Categories.objects.get(slug=slug)
    serializer = CategoryDetailSerializer(categories)
    return Response(serializer.data)

