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
        # Get the latest Home instance (ensure this is correct for your use case)
        user = Home.objects.latest('submitted_at')

        # Retrieve the number of floors and staircase information from the form
        floor_quantity = int(request.POST.get('floor_quantity', 0))
        staircase_quantity = int(request.POST.get('staircase_quantity', 0))

        # Determine if a staircase exists based on user input
        staircase_exists = bool(staircase_quantity)

        # Loop through each floor number
        for floor_num in range(1, floor_quantity + 1):
            # Create or update the Floor instance
            floor, created = Floor.objects.get_or_create(
                user_name=user,
                floor_number=floor_num,
                defaults={'staircase': staircase_exists}
            )

            # If the floor already exists, update its staircase status
            if not created:
                floor.staircase = staircase_exists
                floor.save()

            # Define room types to iterate over
            room_types = ['bedroom', 'living', 'kitchen', 'bathroom', 'parking', 'puja', 'laundry', 'store']

            # Loop through each room type to get quantities and flooring types
            for room in room_types:
                # Retrieve quantity and flooring type for this specific floor
                quantity = int(request.POST.get(f'{room}_quantity_floor{floor_num}', 0))  # Ensure to use the correct key
                flooring = request.POST.get(f'{room}_flooring_floor{floor_num}', 'none')  # Ensure to use the correct key

                # Only create or update Room instances if quantity is greater than zero
                if quantity > 0:
                    Room.objects.update_or_create(
                        user_name=user,
                        floor=floor,
                        room_type=room,
                        defaults={'quantity': quantity, 'flooring_type': flooring}
                    )

        return redirect('other')  # Redirect after processing

    return render(request, 'flooring.html')


# def FlooringView(request):
#     if request.method == 'POST':
#         floor_quantity = int(request.POST.get('floor_quantity', 1))
#         staircase_quantity = int(request.POST.get('staircase_quantity', 0))

#         # Initialize a list to hold the data for each floor
#         floors_data = []

#         for floor in range(1, floor_quantity + 1):
#             # Retrieve quantities and flooring types for each room type per floor
#             # bedrooms_quantity = int(request.POST.get(f'bedroom_quantity', 0))
#             bedrooms_quantity = int(request.POST.get(f'bedroom_quantity_floor{floor}', 0))
#             bedrooms_flooring = request.POST.get(f'bedroom_flooring_floor{floor}', 'none')

#             living_quantity = int(request.POST.get(f'living_quantity_floor{floor}', 0))
#             living_flooring = request.POST.get(f'living_flooring_floor{floor}', 'none')

#             kitchen_quantity = int(request.POST.get(f'kitchen_quantity_floor{floor}', 0))
#             kitchen_flooring = request.POST.get(f'kitchen_flooring_floor{floor}', 'none')

#             bathroom_quantity = int(request.POST.get(f'bathroom_quantity_floor{floor}', 0))
#             bathroom_flooring = request.POST.get(f'bathroom_flooring_floor{floor}', 'none')

#             parking_quantity = int(request.POST.get(f'parking_quantity_floor{floor}', 0))
#             parking_flooring = request.POST.get(f'parking_flooring_floor{floor}', 'none')

#             puja_quantity = int(request.POST.get(f'puja_quantity_floor{floor}', 0))
#             puja_flooring = request.POST.get(f'puja_flooring_floor{floor}', 'none')

#             laundry_quantity = int(request.POST.get(f'laundry_quantity_floor{floor}', 0))
#             laundry_flooring = request.POST.get(f'laundry_flooring_floor{floor}', 'none')

#             store_quantity = int(request.POST.get(f'store_quantity_floor{floor}', 0))
#             store_flooring = request.POST.get(f'store_flooring_floor{floor}', 'none')

#             # Collect data for this floor
#             floor_data = {
#                 "floor": floor,
#                 "bedrooms": {"quantity": bedrooms_quantity, "flooring": bedrooms_flooring},
#                 "living": {"quantity": living_quantity, "flooring": living_flooring},
#                 "kitchen": {"quantity": kitchen_quantity, "flooring": kitchen_flooring},
#                 "bathroom": {"quantity": bathroom_quantity, "flooring": bathroom_flooring},
#                 "parking": {"quantity": parking_quantity, "flooring": parking_flooring},
#                 "puja": {"quantity": puja_quantity, "flooring": puja_flooring},
#                 "laundry": {"quantity": laundry_quantity, "flooring": laundry_flooring},
#                 "store": {"quantity": store_quantity, "flooring": store_flooring},
#             }

#             floors_data.append(floor_data)

#         print("Floor Data:", floors_data)  # Debugging output

#         return redirect('flooring')  # Redirect after processing

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


