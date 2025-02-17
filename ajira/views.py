from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *

# Create your views here.
def HomeView(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        land_area = request.POST.get('size')
        ground_coverage = request.POST.get('ground_coverage')
        construction_standard = request.POST.get('construction_standard')

        new_home = Home(
            name=name,
            land_area=land_area,
            ground_coverage=ground_coverage,
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

        if district_id and municipality_id and home:
            district = District.objects.get(id=district_id)
            municipality = Municipality.objects.get(id=municipality_id)

            Location.objects.create(home=home, district=district, municipality=municipality)
            return redirect("flooring")

    return render(request, "location.html", {"districts": districts})


def Flooring(request):
    return render(request, 'flooring.html')

def Other(request):
    return render(request, 'other.html')

def SpaceCalculation(request):
    return render(request, 'space_cal.html')

def CostCalculation(request):
    return render(request, 'cost_cal.html')


