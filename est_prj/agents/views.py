from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from agents.models import *
from core.models import *
# from django.db.models import Avg
from math import floor
from django.db import models
from . forms import *


from django.contrib import messages
from core.forms import ScheduleTourForm















        # AGENT LIST
def agents(request):
    agents = Agent.objects.filter(verified=True)

    


    context = {
        'agents':agents,
    }

    return render(request, 'agent/agents.html', context)



###########################################################################################################################

        # AGENT DETAILS 
def agent_details(request, agent_id):
    if request.user.is_authenticated:
        agent = Agent.objects.get(agent_id=agent_id, verified=True)
        agent_rating = AgentReview.objects.filter(agent=agent).aggregate(avg_rating=models.Avg('rating'))['avg_rating']
        
        agent_rating = round(agent_rating) if agent_rating is not None else 0
    

        reviews = AgentReview.objects.filter(agent=agent).order_by('-id')
        review_exist = AgentReview.objects.filter(user=request.user, agent=agent).exists()

    else:
        agent = Agent.objects.get(agent_id=agent_id, verified=True)
        agent_rating = AgentReview.objects.filter(agent=agent).aggregate(avg_rating=models.Avg('rating'))['avg_rating']
        
        agent_rating = round(agent_rating) if agent_rating is not None else 0
    

        reviews = AgentReview.objects.filter(agent=agent).order_by('-id')
        review_exist = None
    

        # Pre-fill email for authenticated users
    initial = {'email': request.user.email if request.user.is_authenticated else '', 'full_name': request.user.profile.full_name or 'Anonymous' if request.user.is_authenticated else '', 'phone': request.user.profile.phone or 'Anonymous' if request.user.is_authenticated else ''}
    # initial = {'email': request.user.email, 'full_name': request.user.get_full_name()}
    form = ScheduleTourForm(request.POST or None, initial=initial)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
        
            if form.is_valid():
                tour = form.save()
                tour.agent = agent
                tour.save()
                
                
                noti = Notification.objects.create(
                    agent=agent,
                    type='Inquiry Message',
                    seen=False,
                )
              
                    
                messages.success(request, 'Your request has been submitted. The agent will contact you soon')
                return redirect('agent:agent_details', agent_id=agent_id)
            else:
                messages.error(request, 'An error occurred')

        
        else:
            # house = House.objects.get(hid=hid, status='live')
            form = None

            messages.error(request, 'You need to be logged in to message agent')
            return redirect('userauths:sign_in')
       


   




    context = {
        'agent':agent,
        'form': form,
        'reviews':reviews,
        'review_exist': review_exist,
        'agent_rating':agent_rating,

    }

    return render(request, 'agent/agent_details.html', context)






        # ADD COMMENT
def add_comment(request, agent_id):
    agent = Agent.objects.get(agent_id=agent_id, verified=True)

    if request.user.is_authenticated:

        if request.method == 'POST':
            review = request.POST.get('comment')
            rating = request.POST.get('rating')

            review = AgentReview.objects.create(
                user= request.user,
                agent= agent,
                review= review,
                rating=rating,
            )


            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success':True,
                    'review': {
                        'id': review.id,
                        'full_name': review.user.profile.full_name,
                        'rating': int(review.rating),
                        'date': review.date.strftime('%Y-%m-%d %H:%M:%S'),
                        'profile_image': review.user.profile.image.url if review.user.profile.image else '/static/assets/img/person/default.jpg'

                    }
                })
            
            messages.success(request, 'Review added')
            return redirect('agent:agent_details', agent.agent_id)
        
        return redirect('agent:agent_details', agent.agent_id)
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success':False, 'error': 'Log in to leave a review'}, status=403)
        
        messages.error(request, 'Log in to leave a review')
        return redirect('userauths:sign_in')
    
        

############################################################################################################################################################


        # AGENT DASHBOARD
@login_required(login_url='userauths:sign_in')
def dashboard(request):
    # user = request.user
    agent = Agent.objects.get(user=request.user, verified=True)

            # Agent Houses Stats
    total_houses = House.objects.filter(agent=agent).count()
    total_house_revenue = House.objects.filter(is_sold=True, agent=agent).aggregate(price= models.Sum('price'))['price']
    houses_sold = House.objects.filter(is_sold=True, agent=agent).count()


            # Apartments Stats
    apartments = Apartment.objects.filter(agent=agent)
    apartment_exists = Apartment.objects.filter(agent=agent).exists()
    # total_apartments = Apartment.objects.filter(agent=agent).count()
    bookings = Booking.objects.filter(apartment__in=apartments, payment_status='Paid')
    occupied_apartments = Apartment.objects.filter(agent=agent, is_available=False).count()
    vacant_apartments = Apartment.objects.filter(agent=agent, is_available=True).count()
    booked_earnings = Booking.objects.filter(payment_status='Paid').aggregate(total= models.Sum('total'))['total']
    active_bookings = Booking.objects.filter(apartment__in=apartments, payment_status='Paid', is_active=True)


    # booked_apartments = Booking.objects.filter(apartment__in=apartments, payment_status='Paid', is_active=True)

    
    

    notis = Notification.objects.filter(agent=agent, seen=False).count()



    context = {
        'total_house_revenue': total_house_revenue,
        'houses_sold': houses_sold,
        'total_houses':total_houses,
        'apartments': apartments,
        'bookings': bookings,
        'agent': agent,
        'notis':notis,
        'occupied_apartments':occupied_apartments,
        'vacant_apartments':vacant_apartments,
        'booked_earnings':booked_earnings,
        'active_bookings':active_bookings,
        'apartment_exists':apartment_exists,


    }

    return render(request, 'agent/dashboard.html', context)

#############################################################

        # AGENT APARTMENT LISTINGS
@login_required(login_url='userauths:sign_in')
def agent_apartments(request):

    agent = Agent.objects.get(user=request.user, verified=True)
    apartments = Apartment.objects.filter(agent=agent).order_by('-id')
    reviews = Review.objects.filter(apartment__in=apartments)
    apartment_rating = Review.objects.filter(apartment__in=apartments, apartment__agent=agent).aggregate(avg_rating= models.Avg('rating'))['avg_rating']
    apartment_rating = round(apartment_rating) if apartment_rating is not None else None
    # booking = Booking.objects.filter(apartment__in=apartments, payment_status='Paid')



    context = {
        'apartments': apartments,
        'reviews': reviews,
        'apartment_rating':apartment_rating,
        

    }

    return render(request, 'agent/agent_apartments.html', context)


#########################################################################3

        # ADD APARTMENT
@login_required(login_url='userauths:sign_in')
def create_apartment(request):

    if request.method == 'POST':
        form = ApartmentForm(request.POST, request.FILES)
        gallery_formset = ApartmentGalleryFormset(request.POST, request.FILES, instance=Apartment())
        interior_formset = ApartmentInteriorFormset(request.POST, instance=Apartment())
        exterior_formset = ApartmentExteriorFormset(request.POST, instance=Apartment())
        rule_formset = ApartmentRuleFormset(request.POST, instance=Apartment())
        safety_formset = ApartmentSafetyFormset(request.POST, instance=Apartment())

        if form.is_valid() and gallery_formset.is_valid() and interior_formset.is_valid() and exterior_formset.is_valid() and rule_formset.is_valid() and safety_formset.is_valid():
            apartment = form.save(commit=False)
            apartment.agent = Agent.objects.get(user=request.user)
            apartments_category, _ = Categories.objects.get_or_create(
                    title='Apartments',
                    defaults={'slug': 'apartments-aiv3'}
                )
            apartment.category = apartments_category
            apartment.is_available = True
            apartment.save()
            # apartment.save()
            form.save_m2m()
            gallery_formset.instance = apartment            
            interior_formset.instance = apartment             
            exterior_formset.instance = apartment             
            rule_formset.instance = apartment
            safety_formset.instance = apartment 

            gallery_formset.save()
            interior_formset.save()
            exterior_formset.save()
            rule_formset.save() 
            safety_formset.save()

            messages.success(request, 'Apartment and related data added successfully!')
            return redirect('agent:agent_apartments')


    else:
        form = ApartmentForm()
        gallery_formset = ApartmentGalleryFormset(instance=Apartment())
        interior_formset = ApartmentInteriorFormset(instance=Apartment())
        exterior_formset = ApartmentExteriorFormset(instance=Apartment())
        rule_formset = ApartmentRuleFormset(instance=Apartment())
        safety_formset = ApartmentSafetyFormset(instance=Apartment())



   

    context = {
        'form': form,
        'gallery_formset': gallery_formset,
        'interior_formset': interior_formset,
        'exterior_formset': exterior_formset,
        'rule_formset': rule_formset,
        'safety_formset': safety_formset,
    }

    return render(request, 'agent/create_apartment.html', context)

##########################################################################################

    # EDIT APARTMENT
@login_required(login_url='userauths:sign_in')
def edit_apartment(request, apt_id):
    apartment = Apartment.objects.get(apt_id=apt_id)

    # Calculate number of extra forms for each formset
    existing_interior_count = ApartmentInteriorFeatures.objects.filter(apartment=apartment).count()
    interior_extra = max(0, 5 - existing_interior_count)

    existing_gallery_count = ApartmentGallery.objects.filter(apartment=apartment).count()
    gallery_extra = max(0, 4 - existing_gallery_count)

    existing_exterior_count = ApartmentExteriorFeatures.objects.filter(apartment=apartment).count()
    exterior_extra = max(0, 5 - existing_exterior_count)

    existing_rule_count = ApartmentRules.objects.filter(apartment=apartment).count()
    rule_extra = max(0, 5 - existing_rule_count)

    existing_safety_count = ApartmentSafety.objects.filter(apartment=apartment).count()
    safety_extra = max(0, 5 - existing_safety_count)


    # Dynamically defined formsets
    ApartmentInteriorFormsetDynamic = inlineformset_factory(
        Apartment, ApartmentInteriorFeatures, form=ApartmentInteriorFeatureForm, 
        extra=interior_extra, can_delete=True, min_num=0, validate_min=False
    )
    ApartmentGalleryFormsetDynamic = inlineformset_factory(
        Apartment, ApartmentGallery, form=ApartmentGalleryForm, 
        extra=gallery_extra, can_delete=True, min_num=0, validate_min=False
    )
    ApartmentExteriorFormsetDynamic = inlineformset_factory(
        Apartment, ApartmentExteriorFeatures, form=ApartmentExteriorFeatureForm, 
        extra=exterior_extra, can_delete=True, min_num=0, validate_min=False
    )
    ApartmentRuleFormsetDynamic = inlineformset_factory(
        Apartment, ApartmentRules, form=ApartmentRuleForm, 
        extra=rule_extra, can_delete=True, min_num=0, validate_min=False
    )
    ApartmentSafetyFormsetDynamic = inlineformset_factory(
        Apartment, ApartmentSafety, form=ApartmentSafetyForm, 
        extra=safety_extra, can_delete=True, min_num=0, validate_min=False
    )
    

    if request.method == 'POST':
        form = ApartmentForm(request.POST, request.FILES, instance=apartment)
        gallery_formset = ApartmentGalleryFormsetDynamic(request.POST, request.FILES, instance=apartment)
        interior_formset = ApartmentInteriorFormsetDynamic(request.POST, instance=apartment)
        exterior_formset = ApartmentExteriorFormsetDynamic(request.POST, instance=apartment)
        rule_formset = ApartmentRuleFormsetDynamic(request.POST, instance=apartment)
        safety_formset = ApartmentSafetyFormsetDynamic(request.POST, instance=apartment)

        if form.is_valid() and gallery_formset.is_valid() and interior_formset.is_valid() and exterior_formset.is_valid() and rule_formset.is_valid() and safety_formset.is_valid():
            form.save()
            gallery_formset.save()
            interior_formset.save()
            exterior_formset.save()
            rule_formset.save() 
            safety_formset.save()

            messages.success(request, 'Apartment and related data updated.')
            return redirect('agent:agent_apartments')


        else:
            messages.error(request, 'An error occurred')

    else:
        form = ApartmentForm(instance=apartment)
        gallery_formset = ApartmentGalleryFormsetDynamic(instance=apartment)
        interior_formset = ApartmentInteriorFormsetDynamic(instance=apartment)
        exterior_formset = ApartmentExteriorFormsetDynamic(instance=apartment)
        rule_formset = ApartmentRuleFormsetDynamic(instance=apartment)
        safety_formset = ApartmentSafetyFormsetDynamic(instance=apartment)



   

    context = {
        'form': form,
        'gallery_formset': gallery_formset,
        'interior_formset': interior_formset,
        'exterior_formset': exterior_formset,
        'rule_formset': rule_formset,
        'safety_formset': safety_formset,
    }

    return render(request, 'agent/edit_apartment.html', context)

############################################################################################

        #DELETE APARTMENT
@login_required(login_url='userauths:sign_in')
def delete_apartment(request, apt_id):
    apartment = Apartment.objects.get(apt_id=apt_id)
    apartment.delete()

    messages.success(request, 'Apartment has been deleted')
    return redirect('agent:agent_apartments')

###########################################################################

        # AGENT HOUSES
@login_required(login_url='userauths:sign_in')
def agent_houses(request):
    agent = Agent.objects.get(user=request.user, verified=True)
    houses = House.objects.filter(agent=agent).order_by('-id')


    context = {
        'houses': houses,
    }


    return render(request, 'agent/agent_houses.html', context)

#############################################################################3


        # CREATE HOUSE 
@login_required(login_url='userauths:sign_in')
def create_house(request):

    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES)
        gallery_formset = HouseGalleryFormset(request.POST, request.FILES, instance=House())
        interior_formset = HouseInteriorFormset(request.POST, instance=House())
        exterior_formset = HouseExteriorFormset(request.POST, instance=House())

        if form.is_valid() and gallery_formset.is_valid() and interior_formset.is_valid() and exterior_formset.is_valid():
            house = form.save(commit=False)
            house.agent = Agent.objects.get(user=request.user)
            house_category, _ = Categories.objects.get_or_create(
                title = 'Modern Houses',
                defaults= {'slug': 'modern-houses'}
            )
            house.category = house_category
            house.save()

            form.save_m2m()
            gallery_formset.instance = house
            interior_formset.instance = house
            exterior_formset.instance = house

            gallery_formset.save()
            interior_formset.save()
            exterior_formset.save()

            messages.success(request, 'House and related data added successfully!')
            return redirect('agent:agent_houses')
        
        else:
             messages.success(request, 'An error occurred.')

    
    else:
        form = HouseForm()
        gallery_formset = HouseGalleryFormset(instance=House())
        interior_formset = HouseInteriorFormset(instance=House())
        exterior_formset = HouseExteriorFormset(instance=House())


    
    context = {
        'form': form,
        'gallery_formset': gallery_formset,
        'interior_formset': interior_formset,
        'exterior_formset': exterior_formset,
        
    }

    return render(request, 'agent/create_house.html', context)

#################################################################3



      # EDIT HOUSE 
@login_required(login_url='userauths:sign_in')
def edit_house(request, hid):
    house = House.objects.get(hid=hid)

    existing_gallery_count = HouseGallery.objects.filter(house=house).count()
    gallery_extra = max(0,4 - existing_gallery_count)

    existing_interior_count = InteriorFeatures.objects.filter(house=house).count()
    interior_extra = max(0,5 - existing_interior_count)

    existing_exterior_count = ExteriorFeatures.objects.filter(house=house).count()
    gallery_extra = max(0,5 - existing_exterior_count)


    HouseGalleryFormsetDynamic = inlineformset_factory(
        House, HouseGallery, form=HouseGalleryForm, extra=interior_extra, can_delete=True, min_num=0, validate_min=False
    )

    HouseInteriorFormsetDynamic = inlineformset_factory(
        House, InteriorFeatures, form=InteriorFeatureForm, extra=interior_extra, can_delete=True, min_num=0, validate_min=False
    )

    HouseExteriorFormsetDynamic = inlineformset_factory(
        House, ExteriorFeatures, form=ExteriorFeatureForm, extra=interior_extra, can_delete=True, min_num=0, validate_min=False
    )







    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES, instance=house)
        gallery_formset = HouseGalleryFormsetDynamic(request.POST, request.FILES, instance=house)
        interior_formset = HouseInteriorFormsetDynamic(request.POST, instance=house)
        exterior_formset = HouseExteriorFormsetDynamic(request.POST, instance=house)

        if form.is_valid() and gallery_formset.is_valid() and interior_formset.is_valid() and exterior_formset.is_valid():
            form.save()
            gallery_formset.save()
            interior_formset.save()
            exterior_formset.save()

            messages.success(request, 'House and related data updated')
            return redirect('agent:agent_houses')
        
        else:
             messages.success(request, 'An error occurred.')

    
    else:
        form = HouseForm(instance=house)
        gallery_formset = HouseGalleryFormsetDynamic(instance=house)
        interior_formset = HouseInteriorFormsetDynamic(instance=house)
        exterior_formset = HouseExteriorFormsetDynamic(instance=house)


    
    context = {
        'form': form,
        'gallery_formset': gallery_formset,
        'interior_formset': interior_formset,
        'exterior_formset': exterior_formset,
        
    }

    return render(request, 'agent/edit_house.html', context)

##################################################################################

  # EDIT HOUSE 
@login_required(login_url='userauths:sign_in')
def delete_house(request,hid):
    house = House.objects.get(hid=hid)
    house.delete()

    messages.success(request, 'House has been deleted')
    return redirect('agent:agent_houses')

#############################################################################################

  # Bookings 
@login_required(login_url='userauths:sign_in')
def bookings(request):
    agent = Agent.objects.get(user=request.user, verified=True)

    apartments = Apartment.objects.filter(agent=agent)
    bookings = Booking.objects.filter(apartment__in=apartments, payment_status='Paid')


    context = {
        'bookings': bookings,
    
    }

    return render(request, 'agent/bookings.html', context)

############################################################################################

        # BOOKING DETAILS
@login_required(login_url='userauths:sign_in')
def booking_details(request, booking_id):

    booking = Booking.objects.get(booking_id=booking_id)


    context = {
        'b': booking,
    
    }

    return render(request, 'agent/booking_details.html', context)

#########################################################################################


        # BOOKING DETAILS
@login_required(login_url='userauths:sign_in')
def notifications(request):
    agent = Agent.objects.get(user=request.user)
    notis = Notification.objects.filter(agent=agent, seen=False).order_by('-id')


    context = {
        'notis': notis,
    
    }

    return render(request, 'agent/notifications.html', context)

#############################################################################

        # CLOSE NOTIFICATION
@login_required(login_url='userauths:sign_in')
def close_notification(request):
    id = request.GET['id']
    notification = Notification.objects.get(id=id)
    notification.seen = True
    notification.save()

    return JsonResponse({'data': 'Marked As Seen'})



        # CREATE AGENT
@login_required(login_url='userauths:sign_in')
def create_agent(request):

    if request.method == 'POST':
        form = AgentForm(request.POST, request.FILES)
        spec_formset = AgentSpecializationFormset(request.POST, instance=Agent())

        if form.is_valid() and spec_formset.is_valid():
            agent = form.save(commit=False)
            agent.user = request.user
            agent.is_available = True
            agent.verified = True
            agent.save()
            form.save_m2m()
            spec_formset.instance = agent

            spec_formset.save()

            messages.success(request, 'Agent account created successfully!')
            return redirect('agent:dashboard')
        else:
            # messages.error(request, 'An error occurred.')
            messages.error(request, 'Error creating agent. Please check the form.')
            print(form.errors, spec_formset.errors)  # Debug to console

    else:
        form = AgentForm()
        spec_formset = AgentSpecializationFormset(instance=Agent())
        

            
    

    context = {
        'form': form,
        'spec_formset':spec_formset
    }


    return render(request, 'agent/create_agent.html', context)

###################################################################################
    
        # EDIT AGENT DETAILS
@login_required(login_url='userauths:sign_in')
def edit_agent_details(request):
    agent = Agent.objects.get(user=request.user)

    existing_spec_formset = AgentSpecialization.objects.filter(agent=agent).count()
    formset_extra = max(0,4 - existing_spec_formset)


    AgentSpecializationFormsetDynamic = inlineformset_factory(
        Agent, AgentSpecialization, form=AgentSpecializationForm, extra=formset_extra, can_delete=True, min_num=0, 
        validate_min=False
    )

    if request.method == 'POST':
        form = AgentEditForm(request.POST, request.FILES, instance=agent)
        spec_formset = AgentSpecializationFormsetDynamic(request.POST, instance=agent)

        if form.is_valid() and spec_formset.is_valid():
            form.save()
            spec_formset.save()

            messages.success(request, 'Details editted')
            return redirect('agent:dashboard')
        else:
            # messages.error(request, 'An error occurred.')
            messages.error(request, 'Error editting details.')
            print(form.errors, spec_formset.errors)  # Debug to console

    else:
        form = AgentEditForm(instance=agent)
        spec_formset = AgentSpecializationFormsetDynamic(instance=agent)
        

            
    

    context = {
        'form': form,
        'spec_formset':spec_formset
    }


    return render(request, 'agent/edit_agent_details.html', context)

#####################################################################################

        # EDIT AGENT DETAILS
@login_required(login_url='userauths:sign_in')
def agent_messages(request):
    messages = ScheduleTour.objects.all().order_by('-id')


    context = {
        'inbox': messages,
        
    }


    return render(request, 'agent/agent_messages.html', context)

    





















        






