from core.models import *
from django import forms
from django.forms import inlineformset_factory
from django.utils.text import slugify
from agents.models import *









class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = [
            'name', 'desc', 'address', 'image', 'bedrooms', 'bathrooms', 'garage',
            'state', 'city', 'price', 'sq_ft', 'acres', 'year_build',
            'status', 'neigbourhood_info'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False  # Make image optional
        self.fields['image'].required = False  # Make image optional
        self.fields['garage'].required = False  # Make garage optional
        self.fields['neigbourhood_info'].required = False
        self.fields['desc'].required = False  # Make image optional
        self.fields['address'].required = False  # Make image optional
        self.fields['bedrooms'].required = False  # Make image optional
        self.fields['bathrooms'].required = False  # Make image optional
        self.fields['state'].required = False  # Make image optional
        self.fields['city'].required = False  # Make image optional
        self.fields['status'].required = False  # Make image optional
        self.fields['year_build'].required = False  # Make image optional
        self.fields['price'].required = False  # Make image optional
        self.fields['sq_ft'].required = False  # Make image optional
        self.fields['acres'].required = False  # Make image optional



class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = [
            'name', 'desc', 'address', 'image', 'bedrooms', 'bathrooms', 'garage',
            'state', 'city', 'price', 'year_build',
            'status', 'neigbourhood_info'
        ]

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False  # Make image optional
        self.fields['image'].required = False  # Make image optional
        self.fields['garage'].required = False  # Make garage optional
        self.fields['neigbourhood_info'].required = False
        self.fields['desc'].required = False  # Make image optional
        self.fields['address'].required = False  # Make image optional
        self.fields['bedrooms'].required = False  # Make image optional
        self.fields['bathrooms'].required = False  # Make image optional
        self.fields['state'].required = False  # Make image optional
        self.fields['city'].required = False  # Make image optional
        self.fields['status'].required = False  # Make image optional
        self.fields['year_build'].required = False  # Make image optional
        self.fields['price'].required = False  # Make image optional



class HouseGalleryForm(forms.ModelForm):
    class Meta:
        model = HouseGallery
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False


HouseGalleryFormset = inlineformset_factory(
    House, HouseGallery, form=HouseGalleryForm, extra=4, can_delete=True, min_num=0, 
    validate_min=False
)



class InteriorFeatureForm(forms.ModelForm):
    class Meta:
        model = InteriorFeatures
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False


HouseInteriorFormset = inlineformset_factory(
    House, InteriorFeatures, form=InteriorFeatureForm, extra=5, can_delete=True, min_num=0, 
    validate_min=False
)




class ExteriorFeatureForm(forms.ModelForm):
    class Meta:
        model = ExteriorFeatures
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False


HouseExteriorFormset = inlineformset_factory(
    House, ExteriorFeatures, form=ExteriorFeatureForm, extra=5, can_delete=True, min_num=0, 
    validate_min=False
)





class ApartmentGalleryForm(forms.ModelForm):
    # image = forms.ImageField(required=False)
    class Meta:
        model = ApartmentGallery
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False


ApartmentGalleryFormset = inlineformset_factory(
    Apartment, ApartmentGallery, form=ApartmentGalleryForm, extra=4, can_delete=False, min_num=0, 
    validate_min=False
)

class ApartmentInteriorFeatureForm(forms.ModelForm):
    # name = forms.CharField(required=False)
    class Meta:
        model = ApartmentInteriorFeatures
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False

ApartmentInteriorFormset = inlineformset_factory(
    Apartment, ApartmentInteriorFeatures, form=ApartmentInteriorFeatureForm, extra=5, can_delete=True, min_num=0, 
    validate_min=False
)

class ApartmentExteriorFeatureForm(forms.ModelForm):
    # name = forms.CharField(required=False)
    class Meta:
        model = ApartmentExteriorFeatures
        fields = ['name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False

ApartmentExteriorFormset = inlineformset_factory(
    Apartment, ApartmentExteriorFeatures, form=ApartmentExteriorFeatureForm, extra=5, can_delete=True, min_num=0, 
    validate_min=False
)

class ApartmentRuleForm(forms.ModelForm):
    # rules = forms.CharField(required=False)
    class Meta:
        model = ApartmentRules
        fields = ['rules']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rules'].required = False

ApartmentRuleFormset = inlineformset_factory(
    Apartment, ApartmentRules, form=ApartmentRuleForm, extra=5, can_delete=True, min_num=0, 
    validate_min=False
)

class ApartmentSafetyForm(forms.ModelForm):
    # safety = forms.CharField(required=False)
    class Meta:
        model = ApartmentSafety
        fields = ['safety']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['safety'].required = False


ApartmentSafetyFormset = inlineformset_factory(
    Apartment, ApartmentSafety, form=ApartmentSafetyForm, extra=5, can_delete=True, min_num=0, 
    validate_min=False
)





class AgentForm(forms.ModelForm):
    # identity_image = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control"}))
    class Meta:
        model = Agent
        fields = ['full_name', 'image', 'cover_img', 'email', 'desc', 'phone', 'country', 'state', 'city', 'mission',
                  'office_name', 'office_address', 'twitter', 'instagram', 'facebook', 'whatsapp', 'identity_type', 
                  'identity_image', 'min_price', 'max_price', 'agent_type', 'years_of_exp'
                  
                  ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark fields as optional to match model null/blank settings
        optional_fields = [
            'image', 'cover_img', 'desc', 'mission', 'office_name', 'office_address', 
            'twitter', 'instagram', 'facebook', 'whatsapp', 'min_price', 'max_price', 
            'years_of_exp'
        ]
        for field in optional_fields:
            self.fields[field].required = False

        # Ensure required fields are validated
        self.fields['full_name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['country'].required = True
        self.fields['state'].required = True
        self.fields['city'].required = True
        self.fields['agent_type'].required = True
        self.fields['identity_type'].required = True
        self.fields['identity_image'].required = True  # Adjust if optional in model



class AgentEditForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['full_name', 'image', 'cover_img', 'email', 'desc', 'phone', 'country', 'state', 'city', 'mission',
                  'office_name', 'office_address', 'twitter', 'instagram', 'facebook', 'whatsapp', 'min_price', 'max_price', 'years_of_exp']
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     optional_fields = [
    #         'image', 'cover_img', 'desc', 'mission', 'office_name', 'office_address', 
    #         'twitter', 'instagram', 'facebook', 'whatsapp', 'min_price', 'max_price', 
    #         'years_of_exp'
    #     ]
    #     for field in optional_fields:
    #         self.fields[field].required = False
    #     self.fields['full_name'].required = True
    #     self.fields['email'].required = True
    #     self.fields['phone'].required = True
    #     self.fields['country'].required = True
    #     self.fields['state'].required = True
    #     self.fields['city'].required = True



class AgentSpecializationForm(forms.ModelForm):
    class Meta:
        model = AgentSpecialization
        fields = ['title', 'about']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['about'].required = False



AgentSpecializationFormset = inlineformset_factory(
    Agent, AgentSpecialization, form=AgentSpecializationForm, extra=4, can_delete=True, min_num=0, 
    validate_min=False
)





