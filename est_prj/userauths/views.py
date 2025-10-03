from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
from userauths.forms import *
from django.contrib.auth import login, authenticate, logout










        # SIGN UP
def sign_up(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already logged in')
        return redirect('core:index')


    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()

        full_name = form.cleaned_data.get('full_name')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone')
        password = form.cleaned_data.get('password1')
        
        


        user = authenticate(email=email, password=password)
        login(request, user)
        messages.success(request, f'Hey, {full_name}, your account was created successfully')
        
        


        profile = Profile.objects.create(full_name=full_name, phone=phone, user=user)

        profile.save
        return redirect('core:index')


    context = {
        'form':form,
    }

    return render(request, 'userauths/sign_up.html', context)


        







        # SIGN IN
def sign_in(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already logged in')
        return redirect('core:index')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')


            user = authenticate(request, email=email, password=password)

            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, f'Welcome back, {request.user.profile.full_name}')
                return redirect('core:index')
            else:
                form.add_error(None, 'Email or Password is incorrect')
        # else:
        #      messages.error(request, 'User does not exist')

    else:
        form = LoginForm()


    
    context = {
        'form': form,
    }


    return render(request, 'userauths/sign_in.html', context)








        # SIGN OUT
def sign_out(request):

    logout(request)
    return redirect('userauths:sign_in')
    






    

