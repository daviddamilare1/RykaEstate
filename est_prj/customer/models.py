from django.db import models
from userauths.models import User
from core.models import Apartment, House, Booking
import shortuuid











def generate_nid():
    alphabet = "abcdefghijklmno12345"  # Custom alphabet
    return f"nid_{shortuuid.ShortUUID(alphabet=alphabet).random(length=5)}"


NOTIFICATION_TYPE = (
    ('Booking Confirmed', 'Booking Confirmed'),
    ('Booking Cancelled', 'Booking Cancelled'),
)
















class HouseBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name="housebookmark", null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "House Bookmark"
    
    def __str__(self):
        if self.house.name:
            return self.house.name
        else:
            return "HouseBookmark"
        




class ApartmentBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="apartmentbookmark", null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Apartment Bookmark"
    
    def __str__(self):
        if self.apartment.name:
            return self.apartment.name
        else:
            return "ApartmentBookmark"
        





    

class Notification(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="customer_notifications" )
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE, default=None)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    seen = models.BooleanField(default=False)
    nid = models.CharField(max_length=20, unique=True, default=generate_nid)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'Notifications'


    def __str__(self):
        return self.type