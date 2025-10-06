from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse

from core.models import *
from userauths.models import Profile
from agents import models as agent_models
from customer import models as customer_models
from django.db.models import Avg



from core.forms import ScheduleTourForm

from datetime import datetime
from django.contrib import messages
import re
import phonenumbers
import stripe
from django.conf import settings
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

















    







        # Houses
def houses(request):
    houses = House.objects.filter(status='live', agent__verified=True, is_sold=False).order_by('-id')
    featured_houses = House.objects.filter(featured=True, status='live', agent__verified=True, is_sold=False).order_by('-id')
    
    
    

    context = {
        'houses': houses,
        'featured_houses':featured_houses
       
    }

    return render(request, 'core/houses.html', context)







        # APARTMENTS
def apartments(request):
    apartments = Apartment.objects.filter(status='live', is_available=True, agent__verified=True).order_by('-id')
    featured_apartments = Apartment.objects.filter(featured=True, status='live', is_available=True, agent__verified=True).order_by('-id')
    
    

    context = {
        'apartments': apartments,
        'featured_apartments':featured_apartments,
       
    }

    return render(request, 'core/apartments.html', context)






        # INDEX
def index(request):

    houses = House.objects.filter(featured=True, status='live', agent__verified=True, is_sold=False)
    apartments = Apartment.objects.filter(featured=True, status='live', is_available=True, agent__verified=True)
    

    context = {
        'houses': houses,
        'apartments':apartments,
    }
    
    return render(request, 'core/index.html', context)







        # HOUSE DETAILS
def house_details(request, hid, agent_id):
    house = House.objects.get(hid=hid, status='live', agent__verified=True)
    agent = Agent.objects.get(agent_id=agent_id, verified=True)
    agent_rating = agent_models.AgentReview.objects.filter(agent=agent).aggregate(avg_rating=Avg('rating'))['avg_rating']
    agent_rating = round(agent_rating) if agent_rating is not None else None
    




    
    

   
        # Pre-fill email for authenticated users
    initial = {'email': request.user.email if request.user.is_authenticated else '', 'full_name': request.user.profile.full_name or 'Anonymous' if request.user.is_authenticated else '', 'phone': request.user.profile.phone or 'Anonymous' if request.user.is_authenticated else ''}
    # initial = {'email': request.user.email, 'full_name': request.user.get_full_name()}
    form = ScheduleTourForm(request.POST or None, initial=initial)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
        
            if form.is_valid():
                tour = form.save(commit=False)
                tour.house = house
                tour.save()



                
                
                noti = agent_models.Notification.objects.create(
                    agent=agent,
                    house=house,
                    type='House Tour',
                    seen=False,
                )
              
                    
                messages.success(request, 'The agent will contact you soon')
                return redirect('core:house_details', hid=house.hid, agent_id=agent_id)
        
        else:
            # house = House.objects.get(hid=hid, status='live')
            form = None

            messages.error(request, 'You need to be logged in to message agent')
            return redirect('userauths:sign_in')
       

    context = {
        'house': house,
        'form': form,
        'agent':agent,
        'agent_rating':agent_rating,
        
    }
    
    return render(request, 'core/house_details.html', context)
    






        # APARTMENT DETAILS
def apt_details(request, apt_id, agent_id):
    if request.user.is_authenticated:
        apartment = Apartment.objects.get(apt_id=apt_id, status='live', agent__verified=True)
        reviews = Review.objects.filter(apartment=apartment).order_by('-id')
        review_exist = Review.objects.filter(user=request.user, apartment=apartment).exists()

        agent = Agent.objects.get(agent_id=agent_id, verified=True)

        agent_rating = agent_models.AgentReview.objects.filter(agent=agent).aggregate(avg_rating=Avg('rating'))['avg_rating']
        agent_rating = round(agent_rating) if agent_rating is not None else None


        apartment_rating = Review.objects.filter(apartment=apartment).aggregate(avg_rating=Avg('rating'))['avg_rating']
        apartment_rating = round(apartment_rating) if apartment_rating is not None else None
    else:
        apartment = Apartment.objects.get(apt_id=apt_id, status='live', agent__verified=True)
        reviews = Review.objects.filter(apartment=apartment).order_by('-id')
        review_exist = None

        agent = Agent.objects.get(agent_id=agent_id, verified=True)

        agent_rating = agent_models.AgentReview.objects.filter(agent=agent).aggregate(avg_rating=Avg('rating'))['avg_rating']
        agent_rating = round(agent_rating) if agent_rating is not None else None


        apartment_rating = Review.objects.filter(apartment=apartment).aggregate(avg_rating=Avg('rating'))['avg_rating']
        apartment_rating = round(apartment_rating) if apartment_rating is not None else None


   
    
    

   
   
       

    context = {
        'apartment': apartment,
        'reviews': reviews,
        'review_exist':review_exist,
        'agent':agent,
        'agent_rating':agent_rating,
        'apartment_rating':apartment_rating,
       
    }
    
    return render(request, 'core/apt_details.html', context)





        # ADD COMMENT
def add_comment(request, apt_id):
    apartment = Apartment.objects.get(apt_id=apt_id, status='live', agent__verified=True)
    
    
    if request.user.is_authenticated:

        if request.method == 'POST':

            review = request.POST.get('comment')
            rating = request.POST.get('rating')

            review = Review.objects.create(
                user=request.user,
                apartment=apartment,
                review=review,
                rating=rating,
                active=True
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'review': {
                        'id': review.id,
                        'full_name': review.user.profile.full_name,
                        'rating': int(review.rating),
                        'review': review.review,
                        'date': review.date.strftime('%Y-%m-%d %H:%M:%S'),
                        'profile_image': review.user.profile.image.url if review.user.profile.image else '/static/assets/img/person/default.jpg'
                    }
                })
            
            messages.success(request, 'Review added')
            return redirect('core:apt_details', apartment.apt_id)
        
        return redirect('core:apt_details', apartment.apt_id)
    
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Log in to leave a review'}, status=403)
        
        messages.error(request, 'Log in to leave a review')
        return redirect('userauths:sign_in')
    


            







#####################v########### BOOKING APARTMENTS FUNCTIONS ###########################################################

        # CHECK APARTMENT AVAILABILITY
def check_apartment_availability(request):

    if request.user.is_authenticated:

        if request.method == 'POST':
            apartment_id = request.POST.get('apartment-id')
            checkin = request.POST.get('check-in')
            checkout = request.POST.get('check-out')
            full_name = request.POST.get('full-name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')



            apartment = Apartment.objects.get(id=apartment_id, status='live', is_available=True)

            # Format the dates
            date_format = '%Y-%m-%d'
            checkin_date = datetime.strptime(checkin, date_format)
            checkout_date = datetime.strptime(checkout, date_format)

                # Check for overlapping bookings
            conflicting_booking = Booking.objects.filter(
                apartment=apartment,
                check_in_date__lte = checkout_date,
                check_out_date__gte = checkin_date,
                is_active = True

            )

            if conflicting_booking.exists():
                messages.error(request, 'Apartment is not available for the selected dates.')
                return redirect('core:apt_details', apartment.apt_id)
            
                    # Calculate the days
            time_difference =  checkout_date - checkin_date 
            total_days = time_difference.days
                # Total payment
            total = apartment.price * total_days


            # Create booking for user
            booking = Booking.objects.create(
                user=request.user,
                apartment = apartment,
                full_name = full_name,
                email = email,
                phone = phone,
                check_in_date = checkin_date,
                check_out_date = checkout_date,
                total_days = total_days,
                payment_status = 'Processing',
                total=total,
                is_active = False
                

            )


            request.session['pending_booking'] = booking.booking_id

            return redirect('core:payment_page', booking.booking_id)

    else:
        messages.error(request, 'Login to book an apartment')
        return redirect('userauths:sign_in')

######################################################################################################################

        # CHECKOUT PAGE
def payment_page(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)




    context = {
        'booking': booking,
        'stripe_publishable_key': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request, 'core/payment_page.html', context)

######################################################################################################################

        # CREATE CHECKOUT SESSION
@csrf_exempt
def create_checkout_session(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        customer_email=booking.email,
        payment_method_types= ['card'],
        line_items=[
            {
                'price_data':{
                    'currency': 'USD',
                    'product_data': {
                        'name':booking.full_name
                    },
                    'unit_amount': int(booking.total * 100)
                }, 
                'quantity': 1
            }
        ],
        mode= 'payment',
        success_url= request.build_absolute_uri(reverse('core:payment_success', args=[booking.booking_id])) + "?session_id={CHECKOUT_SESSION_ID}&success_id="+booking.success_id+"&booking_total="+str(booking.total),
        cancel_url= request.build_absolute_uri(reverse('core:payment_failed', args= [booking.booking_id]))
    )

    booking.payment_status = 'Processing'
    booking.stripe_payment_intent = checkout_session['id']
    booking.save()

    print('checkout session', checkout_session)
    return JsonResponse({'sessionId': checkout_session.id})

######################################################################################################################
        
        # PAYMENT SUCCESS
def payment_success(request, booking_id):
    success_id = request.GET.get('success_id')
    booking_total = request.GET.get('booking_total')


    if success_id and booking_total:
        success_id = success_id.rstrip('/')
        booking_total = booking_total.rstrip('/')

        booking = Booking.objects.get(booking_id=booking_id, success_id=success_id)


        if booking.total == Decimal(booking_total):
            if booking.payment_status == 'Processing':
                booking.payment_status = 'Paid'
                booking.is_active = True
                booking.save()
                



                notification = customer_models.Notification.objects.create(
                    customer=request.user,
                    booking=booking, 
                    type= 'Booking Confirmed'

                )

                notification.save()

                noti = agent_models.Notification.objects.create(
                    agent=booking.apartment.agent,
                    apartment=booking.apartment,
                    type='Apartment Booked',
                    seen=False,
                )


                

                if 'pending_booking' in request.session:
                    del request.session['pending_booking']
                
                messages.success(request, 'Payment is successful')
                return redirect('core:index')


            elif booking.payment_status == 'Paid':
                messages.success(request, 'Your booking has been completed')



            else:
                messages.error(request, 'Opps... Internal Server Error; please try again later')
                booking.payment_status = 'Processing'
                booking.save()
                return redirect('core:payment_page', booking_id=booking_id)

        else:
            messages.error(request, 'Error: Payment manipulation detected. ')
            booking.payment_status = 'Failed'
            booking.save()
            return redirect('/')
        
    else:
        messages.error(request, 'Error: Payment manipulation detected. This booking has been cancelled')
        booking = Booking.objects.get(booking_id=booking_id, success_id=success_id)
        booking.payment_status == 'Failed'
        booking.save()
        return redirect('/') 
    


    context = {
        'booking': booking
    }



    return render(request, 'core/payment_success.html', context)

######################################################################################################################

        # PAYMENT FAILED
def payement_failed(request, booking_id):

    booking = Booking.objects.get(booking_id=booking_id)
    booking.payment_status = "Failed"
    booking.save()
                
    context = {
        "booking": booking, 
    }
    
    return render (request, 'core/payment_failed.html', context)
    
######################################################################################################################
            
            # UPDATE APARTMENT STATUS
@csrf_exempt
def update_apartment_status(request):
    
    today = timezone.now().date()


    booking = Booking.objects.filter(is_active=True, payment_status='Paid')

    for b in booking:
        # if checked in tracker is not True and check in date has not reached the date 
        if b.checked_in_tracker != True:
            # (checkin date is still in the future)
            if b.check_in_date > today :
                b.checked_in = False
                b.is_active=True
                b.apartment.is_available = True
                b.apartment.save()
                b.save()

               

            else:
                b.check_in_date = today 
                b.checked_in_tracker = True
                b.checked_in = True
                b.is_active=True
                b.apartment.is_available = False
                b.apartment.save()
                b.save()
                

               
        else:
            if b.check_out_date > today:
                b.checked_out = False
                b.is_active=True
                b.apartment.is_available = False
                b.apartment.save()
                b.save()

               

            else:
                b.check_out_date = today
                b.checked_out_tracker = True
                b.checked_out = True
                b.is_active=False
                b.apartment.is_available = True
                b.apartment.save()
                b.save()

                

    return HttpResponse(today)








       
       




                





        









