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
    list_display = ('home','district', 'municipality', 'submitted_at')
    search_fields = ('district', 'municipality')

@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('home','number',)
    list_filter = ('number',)
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'floor', 'quantity', 'flooring_type')
    list_filter = ('room_type', 'flooring_type')
    search_fields = ('room_type',)

@admin.register(Other)
class AdditionalFeatureAdmin(admin.ModelAdmin):
    list_display = ('home', 'compound_flooring', 'staircase_flooring', 'window_type')
    list_filter = ('compound_flooring', 'staircase_flooring', 'window_type')
    
