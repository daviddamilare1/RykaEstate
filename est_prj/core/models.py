from django.db import models
import shortuuid
from django.utils.html import mark_safe
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from agents.models import Agent
from userauths.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import uuid















def generate_house_gallery_id():
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890"  # Custom alphabet
    return f"hgid_{shortuuid.ShortUUID(alphabet=alphabet).random(length=7)}" 





def generate_apartment_gallery_id():
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890"  # Custom alphabet
    return f"agid_{shortuuid.ShortUUID(alphabet=alphabet).random(length=7)}" 


def generate_house_id():
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890"  # Custom alphabet
    return f"hid_{shortuuid.ShortUUID(alphabet=alphabet).random(length=7)}" 



def generate_apt_id():
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890"  # Custom alphabet
    return f"apt_{shortuuid.ShortUUID(alphabet=alphabet).random(length=7)}" 


def generate_booking_id():
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890"  # Custom alphabet
    return f"bid_{shortuuid.ShortUUID(alphabet=alphabet).random(length=7)}" 




def generate_success_id():
    return f"sid_{str(uuid.uuid4())[:7]}"

######################### CHOICES ###############################################

ICON_TYPE = [
    ('bootstrap icons', 'Bootstrap Icons'),
    ('fontawesome icons', 'Fontawesome Icons'),
    ('box icons', 'Box Icons'),
    ('remi icons', 'Remi Icons'),
    ('flat icons', 'Flat Icons'),

]


HOUSE_STATUS = [
    ('draft', 'Draft'),
    ('rejected', 'Rejected'),
    ('in review', 'In Review'),
    ('live', 'Live'),

]


STATE = [
    ('Abia', 'Abia'),
    ('Oyo', 'Oyo'),
    ('Plateau', 'Plateau'),
    ('Kwara', 'Kwara'),
    ('Lagos', 'Lagos'),
    
]


CITY = [
    ('Umuahia', 'Umuahia'),
    ('Ibadan', 'Ibadan'),
    ('Jos', 'Jos'),
    ('Ilorin', 'Ilorin'),
    ('Ikeja', 'Ikeja'),
    
]



PAYMENT_STATUS = (
    ("Paid", "Paid"),
    ("Processing", "Processing"),
    ("Failed", 'Failed'),
    # ('Pending', 'Pending'),
)


RATING = (
    ( 1,  "★☆☆☆☆"),
    ( 2,  "★★☆☆☆"),
    ( 3,  "★★★☆☆"),
    ( 4,  "★★★★☆"),
    ( 5,  "★★★★★"),
)



PAYMENT_METHOD = (
    ("PayPal", "PayPal"),
    ("Stripe", "Stripe"),
    ("Flutterwave", "Flutterwave"),
    ("Paystack", "Paystack"),
    ("RazorPay", "RazorPay"),
)














class Categories(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(default='category.jpg', null=True, blank=True, upload_to='images')
    slug = models.SlugField(unique=True, blank=True)


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Categories"
    

    def category_image(self):
        return mark_safe('<img src="%s" width="50px" height="50px" style="object-fit: cover; border-radius: 6px;" />' % (self.image.url) )
    

    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            uuid_key = shortuuid.uuid()
            unique_id = uuid_key[:4]
            self.slug = slugify(self.title) + '-' + str(unique_id.lower())

        super(Categories, self).save(*args, **kwargs)
    

    # def save(self, *args, **kwargs):
    #     """Override save to generate a unique slug if not provided."""
    #     if not self.slug:
    #         # Generate a base slug from the title
    #         base_slug = slugify(self.title)
    #         slug = base_slug
    #         counter = 1
    #         # Ensure the slug is unique by appending a counter if necessary
    #         while Categories.objects.filter(slug=slug).exclude(pk=self.pk).exists():
    #             slug = f"{base_slug}-{counter}"
    #             counter += 1
    #         self.slug = slug
    #     super().save(*args, **kwargs)
    

    






class House(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='house')
    name = models.CharField(max_length=255)
    desc = models.TextField(max_length=700)
    address = models.CharField(max_length=100)
    image = models.FileField(upload_to='house_gallery')

    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    garage = models.PositiveIntegerField(null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)

    state = models.CharField(max_length=20, choices=STATE, default=None)
    city = models.CharField(max_length=100, choices=CITY, default=None, null=True, blank=True)

    price = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)

    sq_ft = models.DecimalField(help_text='Enter the size in square feet', decimal_places=2, max_digits=10)
    acres = models.DecimalField(help_text='Enter the size in acres', decimal_places=2, max_digits=10)
    
    featured = models.BooleanField(default=False)
    year_build = models.IntegerField(help_text='Enter the year')
    date = models.DateTimeField(auto_now_add=True)

    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=20, choices=HOUSE_STATUS, default='draft')
    hid = models.CharField(max_length=20, unique=True, default=generate_house_id)
    is_sold = models.BooleanField(default=False)
    neigbourhood_info = models.TextField(max_length=255, null=True, blank=True)
    h_type = models.CharField(max_length=255, null=True, blank=True)





    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name_plural = "Houses"


    def house_image(self):
        return mark_safe('<img src="%s" width="50px" height="50px" style="object-fit: cover; border-radius: 6px;" />' % (self.image.url) )

    ## Make sure there isn't more than one house with the same name by generating a uuid for the copy house
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            uuid_key = shortuuid.uuid()
            unique_id = uuid_key[:4]
            self.slug = slugify(self.name) + '-' + str(unique_id.lower())

        super(House, self).save(*args, **kwargs)



    def house_gallery(self):
        return HouseGallery.objects.filter(house=self)
    

    def interior_features(self):
        return InteriorFeatures.objects.filter(house=self)
    


    def exterior_features(self):
        return ExteriorFeatures.objects.filter(house=self)


    

    






class HouseGallery(models.Model):
    house = models.ForeignKey(House, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='house_gallery')
    hgid = models.CharField(max_length=20, unique=True, default=generate_house_gallery_id)



    def __str__(self):
        return str(self.house.name)
    
    class Meta:
        verbose_name_plural = 'House Gallery'






class InteriorFeatures(models.Model):
    house = models.ForeignKey(House, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)



    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = 'Interior Features'






class ExteriorFeatures(models.Model):
    house = models.ForeignKey(House, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)



    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = 'Exterior Features'







class Apartment(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='apartment')
    name = models.CharField(max_length=255)
    desc = models.TextField(max_length=700)
    address = models.CharField(max_length=100)
    image = models.FileField(upload_to='apartment_gallery')

    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    garage = models.PositiveIntegerField(null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)

    state = models.CharField(max_length=20, choices=STATE, default=None)
    city = models.CharField(max_length=100, choices=CITY, default=None, null=True, blank=True)

    price = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)

    sq_ft = models.DecimalField(help_text='Enter the size in square feet', decimal_places=2, max_digits=10, null=True, blank=True)
    acres = models.DecimalField(help_text='Enter the size in acres', decimal_places=2, max_digits=10, null=True, blank=True)
    
    featured = models.BooleanField(default=False)
    year_build = models.IntegerField(help_text='Enter the year')
    date = models.DateTimeField(auto_now_add=True)

    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=20, choices=HOUSE_STATUS, default='draft')
    apt_id = models.CharField(max_length=20, unique=True, default=generate_apt_id)
    is_available = models.BooleanField(default=False)
    neigbourhood_info = models.TextField(max_length=255, null=True, blank=True)
    a_type = models.CharField(max_length=255, null=True, blank=True)



    class Meta:
        verbose_name_plural = 'Apartments'

    def __str__(self):
        return self.name




    def apartment_image(self):
        return mark_safe('<img src= "%s" width="50" height="50" />' % (self.image.url))


    def apartment_gallery(self):
        return ApartmentGallery.objects.filter(apartment=self)
    
    def apartment_interior(self):
        return ApartmentInteriorFeatures.objects.filter(apartment=self)
    
    def apartment_exterior(self):
        return ApartmentExteriorFeatures.objects.filter(apartment=self)
    

    def apartment_rules(self):
        return ApartmentRules.objects.filter(apartment=self)
    
    def apartment_safety(self):
        return ApartmentSafety.objects.filter(apartment=self)
    
    def average_rating(self):
        return Review.objects.filter(apartment=self).aggregate(avg_rating=models.Avg('rating'))['avg_rating']




    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            uuid_key = shortuuid.uuid()
            unique_id = uuid_key[:4]
            self.slug = slugify(self.name) + '-' + str(unique_id.lower())

        super(Apartment, self).save(*args, **kwargs)









class ApartmentGallery(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='apartment_gallery')
    agid = models.CharField(max_length=20, unique=True, default=generate_apartment_gallery_id)



    def __str__(self):
        return str(self.apartment.name)
    
    class Meta:
        verbose_name_plural = 'Apartment Gallery'





class ApartmentInteriorFeatures(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = 'Apartment Interior'





    

class ApartmentExteriorFeatures(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = 'Apartment Exterior'





class ApartmentRules(models.Model):
    rules = models.CharField(max_length=100, null=True, blank=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return str(self.rules)
    
    class Meta:
        verbose_name_plural = 'Apartment Rules'



class ApartmentSafety(models.Model):
    safety = models.CharField(max_length=100, null=True, blank=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return str(self.safety)
    
    class Meta:
        verbose_name_plural = 'Apartment Safety'





class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD, default=None, null=True, blank=True)


    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)

    apartment = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    check_in_date = models.DateField()
    check_out_date = models.DateField()

    total_days = models.PositiveIntegerField(default=0)

    checked_in = models.BooleanField(default=False)
    checked_out = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)


    checked_in_tracker = models.BooleanField(default=False)
    checked_out_tracker = models.BooleanField(default=False)

    date =  models.DateTimeField(auto_now_add=True)
    booking_id = models.CharField(max_length=20, unique=True, default=generate_booking_id)
    # success_id = models.UUIDField(default=uuid.uuid4, unique=True, null=True, blank=True)
    success_id = models.CharField(max_length=20, unique=True, default=generate_success_id)
    stripe_payment_intent = models.CharField(max_length=1000, null=True, blank=True)



    def __str__(self):
        return f'{self.booking_id}'
    
    # Count the rooms
    # def apartments(self):
    #     return self.apartment.all().count()





class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.SET_NULL, blank=True, null=True, related_name="reviews")
    review = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)
    rating = models.IntegerField(choices=RATING, default=None)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} review on {self.apartment.name}"
    

    class Meta:
        verbose_name_plural = 'Apartment Reviews' 






# class HouseReview(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
#     house = models.ForeignKey(House, on_delete=models.SET_NULL, blank=True, null=True, related_name="reviews")
#     review = models.TextField(null=True, blank=True)
#     reply = models.TextField(null=True, blank=True)
#     rating = models.IntegerField(choices=RATING, default=None)
#     active = models.BooleanField(default=False)
#     date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} review on {self.house.name}"
    

#     class Meta:
#         verbose_name_plural = 'House Reviews' 









class ScheduleTour(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=1)
    full_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    message = models.CharField(max_length=60)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.email}"










    
    


    



