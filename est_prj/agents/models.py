from django.db import models
from userauths.models import User
from django.utils.html import mark_safe
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
import shortuuid
from core.models import *













def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (instance.user.id, filename)
    return 'agents_{0}/{1}'.format(instance.user.id, filename)


def broker_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (instance.user.id, filename)
    return 'brokers_{0}/{1}'.format(instance.user.id, filename)

############################################################################################

def generate_aid():
    alphabet = "abcdefghijklmno12345"  # Custom alphabet
    return f"aid_{shortuuid.ShortUUID(alphabet=alphabet).random(length=5)}"


def generate_bid():
    alphabet = "abcdefghijklmno12345"  # Custom alphabet
    return f"bid_{shortuuid.ShortUUID(alphabet=alphabet).random(length=5)}"


def generate_nid():
    alphabet = "abcdefghijklmno12345"  # Custom alphabet
    return f"nid_{shortuuid.ShortUUID(alphabet=alphabet).random(length=5)}"





############################## CHOICES ######################################################

IDENTITY_TYPE = (
    ('National Identification number', 'National Identification Number'),
    ("Driver's License", "Driver's License"),
    ('International Passport', 'International Passport'),
)




AGENT_TYPE = (
    ('Realtor', 'Realtor'),
    ('Property Manager', 'Property Manager'),
    ('Property Owner', 'Property Owner'),
    ('Leasing Agent', 'Leasing Agent'),
    

)


NOTIFICATION_TYPE = (
    ('House Tour', 'House Tour'),
    ('Inquiry Message', 'Inquiry Message'),
    ('Apartment Booked', 'Apartment Booked'),
    ('Property Approved', 'Property Approved'),
    ('Property Rejected', 'Property Rejected'),
    ('Verification Updated', 'Verification Updated'),
)





RATING = (
    ( 1,  "★☆☆☆☆"),
    ( 2,  "★★☆☆☆"),
    ( 3,  "★★★☆☆"),
    ( 4,  "★★★★☆"),
    ( 5,  "★★★★★"),
)


















class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name='agents')

    full_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='agent_images', default='agent.jpg')
    cover_img = models.ImageField(upload_to='agent_cover_images', default='agent_cover.jpg')

    email = models.EmailField(unique=True)
    desc = models.CharField(max_length=700)
    phone = models.CharField(max_length=11)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    mission = models.CharField(max_length=200, null=True, blank=True)

    office_name = models.CharField(max_length=200, null=True, blank=True)
    office_address = models.CharField(max_length=200, null=True, blank=True)

    twitter = models.URLField(max_length=200, null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    whatsapp = models.URLField(max_length=200, null=True, blank=True)
    

   
    identity_type = models.CharField(max_length=100,choices=IDENTITY_TYPE)
    identity_image = models.FileField(upload_to=user_directory_path, default='id.jpg')
    verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)

    min_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    agent_id = models.CharField(max_length=20, unique=True, default=generate_aid)
    agent_type = models.CharField(max_length=100,choices=AGENT_TYPE)
    date = models.DateTimeField(auto_now_add=True)
    years_of_exp = models.IntegerField(help_text='How many years')



    def agent_image(self):
        return mark_safe('<img src= "%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.full_name
    

    def agent_specialties(self):
        return AgentSpecialization.objects.filter(agent=self)
    

    def agent_average_rating(self):
        return AgentReview.objects.filter(agent=self).aggregate(avg_rating=models.Avg('rating'))['avg_rating']
    

    class Meta:
        verbose_name_plural = "Agents"





class AgentSpecialization(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='agent')
    title = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(max_length=100, null=True, blank=True)



    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name_plural = 'Agent Specialties'
    



class AgentReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, blank=True, null=True, related_name="reviews")
    review = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)
    rating = models.IntegerField(choices=RATING, default=None)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} review on {self.agent.full_name}"
    


    
    

    class Meta:
        verbose_name_plural = 'Agent Reviews' 



    
    










class BrokerAgent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name='brokers')

    full_name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='agent_images', default='agent.jpg')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    office_name = models.URLField(max_length=200, null=True, blank=True)
    office_address = models.URLField(max_length=200, null=True, blank=True)

    twitter = models.URLField(max_length=200, null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    whatsapp = models.URLField(max_length=200, null=True, blank=True)
   

    identity_type = models.FileField(max_length=100,choices=IDENTITY_TYPE)
    identity_image = models.FileField(upload_to=broker_directory_path, default='id.jpg')

    verified = models.BooleanField(default=False)
    broker_id = models.CharField(max_length=20, unique=True, default=generate_bid)
    date = models.DateTimeField(auto_now_add=True)
    years_of_exp = models.IntegerField(help_text='How many years')



    class Meta:
        verbose_name_plural = "Brokers"

    def __str__(self):
        return self.full_name





class Notification(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, blank=True, related_name="agent_notifications" )
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE, default=None)
    house = models.ForeignKey('core.House', on_delete=models.CASCADE, null=True, blank=True)
    apartment = models.ForeignKey('core.Apartment', on_delete=models.CASCADE, null=True, blank=True)
    seen = models.BooleanField(default=False)
    nid = models.CharField(max_length=20, unique=True, default=generate_nid)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'Notifications'


    def __str__(self):
        return self.type
