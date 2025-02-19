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
    list_display = ('user_name','floor', 'room_type', 'quantity', 'flooring_type','room_area','rate','cost')
    list_filter = ('room_type', 'flooring_type')
    search_fields = ('room_type',)

@admin.register(Other)
class OtherAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'compound_flooring', 'staircase_flooring', 'window_type')
    list_filter = ('compound_flooring', 'staircase_flooring', 'window_type')
    
@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('user_name','phone_number','total_house_area')
    
@admin.register(Cost)
class CostAdmin(admin.ModelAdmin):
    list_display = ('user_name','total_cost',)
    
