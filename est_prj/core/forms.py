from django import forms
import re
from core.models import ScheduleTour













try:
    import phonenumbers
except ImportError:
    phonenumbers = None







class ScheduleTourForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control rounded', 'placeholder':'Enter Full Name'}), required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control rounded', 'placeholder':'Enter Phone Number'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control rounded', 'placeholder':'Enter Email'}), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control rounded', 'placeholder':'Write a brief message for the agent'}), required=True)



    class Meta:
        model = ScheduleTour
        fields = ['full_name', 'email', 'phone', 'message']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.lower().endswith('@gmail.com'):
            raise forms.ValidationError('Please enter a valid email address.')
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