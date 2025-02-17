from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import *

# Create your views here.
def HomeView(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        land_area = request.POST.get('size')  
        ground_coverage = request.POST.get('ground_coverage')
        construction_standard = request.POST.get('construction_standard')

        land_area_map = {
            '2.5-3.0': 3.0,
            '3.0-3.5': 3.5,
            '3.5-4.0': 4.0,
            '4.0-4.5': 4.5,
            '4.5-5.0': 5.0,
            '> 5.0': 20 
        }

        land_area_max_limit = land_area_map[land_area]
        max_perm_ground_coverage = land_area_max_limit * 342.25 * 0.7
    
        try:
            ground_coverage_value = float(ground_coverage)
        except ValueError:
            messages.error(request, "Invalid ground coverage input.")
            return redirect('home')

        if ground_coverage_value > max_perm_ground_coverage:
            messages.error(request, f"Ground coverage must not exceed 70% of the land.")
            return redirect('home')

        new_home = Home(
            name=name,
            land_area=land_area,
            ground_coverage=ground_coverage_value,
            construction_standard=construction_standard
        )
        new_home.save()
        return redirect('location')
    return render(request, 'home.html')


def get_municipalities(request, district_id):
    municipalities = Municipality.objects.filter(district_id=district_id).values("id", "name")
    return JsonResponse(list(municipalities), safe=False)


def LocationView(request):
    districts = District.objects.all()
    
    home = Home.objects.latest('submitted_at') 

    if request.method == "POST":
        district_id = request.POST.get("district")
        municipality_id = request.POST.get("local-body")
        contact_number_id = request.POST.get("contact_number")

        if district_id and municipality_id and home:
            district = District.objects.get(id=district_id)
            municipality = Municipality.objects.get(id=municipality_id)

            Location.objects.create(home=home, district=district, municipality=municipality, contact_number=contact_number_id)
            return redirect("flooring")

    return render(request, "location.html", {"districts": districts})


def Flooring(request):
    return render(request, 'flooring.html')

def Other(request):
    return render(request, 'other.html')

def Summary(request):
    return render(request, 'summary.html')

def CostCalculation(request):
    return render(request, 'cost_cal.html')


