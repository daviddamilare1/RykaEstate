from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
import re
try:
    import phonenumbers
except ImportError:
    phonenumbers = None

from userauths.models import *





# USER_TYPE = (
#     ('Vendor', 'Vendor'),
#     ('Customer', 'Customer'),

# )



class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control rounded', 'placeholder':'Full Name'}), required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control rounded', 'placeholder':'Phone Number'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control rounded', 'placeholder':'Email'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control rounded', 'placeholder':'Password'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control rounded', 'placeholder':'Confirm Password'}), required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    # user_type = forms.ChoiceField(choices=USER_TYPE, widget=forms.Select(attrs={'class': 'form-select'}))


    class Meta:
        model = User
        fields = ['full_name','phone',  'email', 'password1', 'password2']

    


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.lower().endswith('@gmail.com'):
            raise forms.ValidationError('Please enter a valid email address.')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address has already been used')
        return email
    

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError('Phone number is required.')

        if phonenumbers:
            try:
                # Parse phone number with Nigeria region code
                parsed_phone = phonenumbers.parse(phone, 'NG')
                # Check if it's a valid Nigerian phone number
                if not (phonenumbers.is_valid_number(parsed_phone) and 
                        phonenumbers.region_code_for_number(parsed_phone) == 'NG'):
                    raise forms.ValidationError('Please enter a valid Nigerian phone number.')
                # Optional: Normalize to international format (+234)
                return phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)
            except phonenumbers.NumberParseException:
                raise forms.ValidationError('Invalid Nigerian phone number format.')
        else:
            # Fallback regex for Nigerian phone numbers
            # Matches: +2348012345678 or 08012345678
            phone_regex = r'^(?:\+234|0)(?:70|80|81|90|91|71)\d{8}$'
            if not re.match(phone_regex, phone):
                raise forms.ValidationError('Please enter a valid Nigerian phone number.')
            # Normalize local format to international if needed
            if phone.startswith('0'):
                phone = '+234' + phone[1:]
            return phone





class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control rounded', 'placeholder':'Email'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control rounded', 'placeholder':'Password'}), required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None or not user.is_active:
                raise forms.ValidationError('Invalid email or password.')
        return cleaned_data