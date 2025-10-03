from django.contrib import admin
from core.models import *










class HouseGalleryInline (admin.TabularInline):
    model = HouseGallery

class HouseInteriorFeaturesInline (admin.TabularInline):
    model = InteriorFeatures


class HouseExteriorFeaturesInline (admin.TabularInline):
    model = ExteriorFeatures




class ApartmentGalleryInline (admin.TabularInline):
    model = ApartmentGallery

class ApartmentInteriorFeaturesInline (admin.TabularInline):
    model = ApartmentInteriorFeatures


class ApartmentExteriorFeaturesInline (admin.TabularInline):
    model = ApartmentExteriorFeatures



class ApartmentAdmin(admin.ModelAdmin):
    inlines = [ApartmentGalleryInline, ApartmentExteriorFeaturesInline, ApartmentInteriorFeaturesInline]
    list_display = ['agent','apartment_image', 'name', 'bedrooms', 'bathrooms', 'category', 'price', 'status']
    list_editable = ['status']
    prepopulated_fields = {'slug':('name',)}


class HouseAdmin(admin.ModelAdmin):
    inlines = [HouseGalleryInline, HouseInteriorFeaturesInline, HouseExteriorFeaturesInline]
    list_display = ['agent', 'house_image', 'name', 'bedrooms', 'bathrooms', 'category', 'price', 'status']
    list_editable = ['status']
    prepopulated_fields = {'slug':('name',)}





class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_image', 'title')
    prepopulated_fields = {'slug': ('title',)}
   

    










admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Booking)
admin.site.register(House, HouseAdmin)
admin.site.register(ExteriorFeatures)
admin.site.register(InteriorFeatures)
admin.site.register(ApartmentExteriorFeatures)
admin.site.register(ApartmentInteriorFeatures)
admin.site.register(HouseGallery)
admin.site.register(Review)
admin.site.register(Categories, CategoryAdmin)
admin.site.register(ScheduleTour)
# admin.site.register(Booking)





