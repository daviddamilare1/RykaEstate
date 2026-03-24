from django.shortcuts import render, redirect
from . models import *


# Create your views here.












def dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    total_spent =  Booking.objects.filter(payment_status='Paid', user=request.user).aggregate(total= models.Sum('total'))['total']


    context = {
        'bookings': bookings,
        'total_spent': total_spent,
    }
    

    return render (request, 'customer/dashboard.html', context)