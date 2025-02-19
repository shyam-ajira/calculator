from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from .forms import *

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
    
    user_name = Home.objects.latest('submitted_at') 

    if request.method == "POST":
        district_id = request.POST.get("district")
        municipality_id = request.POST.get("local-body")
        contact_number_id = request.POST.get("contact_number")

        if district_id and municipality_id and user_name:
            district = District.objects.get(id=district_id)
            municipality = Municipality.objects.get(id=municipality_id)

            Location.objects.create(user_name=user_name, district=district, municipality=municipality, contact_number=contact_number_id)
            return redirect("flooring")

    return render(request, "location.html", {"districts": districts})



def FlooringView(request):
    if request.method == 'POST':
        user = Home.objects.latest('submitted_at') 

        floor_quantity = int(request.POST.get('floor_quantity', 0))
        staircase_quantity = request.POST.get('staircase_quantity', 0)

        staircase_exists = bool(int(staircase_quantity))

        for floor_num in range(1, floor_quantity + 1):
            floor, created = Floor.objects.get_or_create(
                user_name=user, floor_number=floor_num,
                defaults={'staircase': staircase_exists} 
            )

            if not created:
                floor.staircase = staircase_exists
                floor.save()

            room_types = [
                'bedroom', 'living', 'kitchen', 'bathroom', 'parking',
                'puja', 'laundry', 'store'
            ]

            for room in room_types:
                quantity = int(request.POST.get(f'{room}_quantity', 0))
                flooring = request.POST.get(f'{room}_flooring', 'none')

                if quantity > 0:
                    Room.objects.update_or_create(
                        user_name=user,
                        floor=floor,
                        room_type=room, 
                        defaults={'quantity': quantity, 'flooring_type': flooring}
                    )

        return redirect('other')

    return render(request, 'flooring.html')

# def FlooringView(request):
#     if request.method == 'POST':

#         # Room quantities and flooring types
#         bedrooms_quantity = request.POST.get('bedrooms_quantity')
#         bedrooms_flooring = request.POST.get('bedrooms_flooring')

#         living_quantity = request.POST.get('living_quantity')
#         living_flooring = request.POST.get('living_flooring')

#         kitchen_quantity = request.POST.get('kitchen_quantity')
#         kitchen_flooring = request.POST.get('kitchen_flooring')

#         bathroom_quantity = request.POST.get('bathroom_quantity')
#         bathroom_flooring = request.POST.get('bathroom_flooring')

#         parking_quantity = request.POST.get('parking_quantity')
#         parking_flooring = request.POST.get('parking_flooring')

#         puja_quantity = request.POST.get('puja_quantity')
#         puja_flooring = request.POST.get('puja_flooring')

#         laundry_quantity = request.POST.get('laundry_quantity')
#         laundry_flooring = request.POST.get('laundry_flooring')

#         store_quantity = request.POST.get('store_quantity')
#         store_flooring = request.POST.get('store_flooring')

#         floor_quantity = request.POST.get('floor_quantity')
#         staircase_quantity = request.POST.get('staircase_quantity')

#         # Print quantities and flooring types
#         print("Bedrooms:", bedrooms_quantity, "Flooring:", bedrooms_flooring)
#         print("Living:", living_quantity, "Flooring:", living_flooring)
#         print("Kitchen:", kitchen_quantity, "Flooring:", kitchen_flooring)
#         print("Bathroom:", bathroom_quantity, "Flooring:", bathroom_flooring)
#         print("Parking:", parking_quantity, "Flooring:", parking_flooring)
#         print("Puja:", puja_quantity, "Flooring:", puja_flooring)
#         print("Laundry:", laundry_quantity, "Flooring:", laundry_flooring)
#         print("Store:", store_quantity, "Flooring:", store_flooring)
#         print("Floors:", floor_quantity)  
#         print("Staircases:", staircase_quantity)

#         return redirect('flooring')
    
#     return render(request, 'flooring.html')


def OtherView(request):
    if request.method == "POST":
        compound_flooring = request.POST.get('compound_flooring')
        staircase_flooring = request.POST.get('staircase_flooring')
        window_type = request.POST.get('window_type')
        user_name = Home.objects.latest('submitted_at')  
        
        Other.objects.create(
            user_name=user_name,
            compound_flooring=compound_flooring,
            staircase_flooring=staircase_flooring,
            window_type=window_type
        )
        return redirect('summary')  
    return render(request, 'other.html')

def Summary(request):
    return render(request, 'summary.html')

def CostCalculation(request):
    return render(request, 'cost_cal.html')


