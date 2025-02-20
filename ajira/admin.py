from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'land_area', 'ground_coverage', 'construction_standard', 'submitted_at')
    search_fields = ('name',)

admin.site.register(District)
admin.site.register(Municipality)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('user_name','district', 'municipality', 'submitted_at')
    search_fields = ('district', 'municipality')

@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('user_name','floor_number','staircase',)
    list_filter = ('floor_number',)
    
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('user_name','floor', 'room_type', 'quantity', 'flooring_type','room_area','rate','cost', 'window_area')
    

@admin.register(Other)
class OtherAdmin(admin.ModelAdmin):
    list_display = ('user_name','phone_number','finish_type','finish','qty','rate','cost')

    
@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('user_name','phone_number','no_of_floors','total_house_area')
    

    
