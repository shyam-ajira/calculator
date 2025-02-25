from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from .forms import *
import datetime
from django.db.models import Sum


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
        
        existing_home = Home.objects.filter(name=name).first()
        if existing_home:
            messages.error(request, "Name already exists.")
            return render(request, 'home.html')

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
        

        for floor_num in range(1, floor_quantity + 1):
            staircase_quantity = int(request.POST.get(f'staircase-{floor_num}',0))
            # staircase_quantity = int(request.POST.get('staircase_quantity', 0))
            staircase_exists = bool(staircase_quantity)     
            floor, created = Floor.objects.get_or_create(
                user_name=user,
                floor_number=floor_num,
                defaults={'staircase': staircase_exists}
            )
            if not created:
                floor.staircase = staircase_exists
                floor.save()

            room_types = ['bedroom', 'living', 'kitchen', 'bathroom', 'parking', 'puja', 'laundry', 'store']
            for room in room_types:
                quantity = int(request.POST.get(f'{room}_quantity_floor{floor_num}', 0))  
                flooring = request.POST.get(f'{room}_flooring_floor{floor_num}', 'none') 
                if quantity > 0:
                    Room.objects.update_or_create(
                        user_name=user,
                        floor=floor,
                        floor_numm = floor_num,
                        room_type=room,
                        defaults={'quantity': quantity, 'flooring_type': flooring}
                    )
               
        return redirect('other') 
    return render(request, 'flooring.html')


def OtherView(request):
    if request.method == "POST":
        user_name = Home.objects.latest('submitted_at')  
        finish_types = ['compound_flooring', 'staircase_flooring', 'window_type','door','paint','main_door','electrical','plumbing','kitchen','bathroom','sani_other','mod_kitchen','landscape','other_metal_works','railing','misc']
        for finish_place in finish_types:
            post_data = request.POST.get(finish_place) 
            if post_data:
                Other.objects.create(
                    user_name=user_name,
                    finish_type=finish_place,
                    finish=post_data   
                )
            else:
                Other.objects.create(
                    user_name=user_name,
                    finish_type=finish_place,
                    finish=finish_place
                )
        return redirect('summary')  
    return render(request, 'other.html')

def SummaryView(request):
    user = Home.objects.latest('submitted_at')
    total_house_area = user.summary.total_house_area
    carpet_area = user.summary.total_carpet_area
    context={
        'total_house_area':total_house_area,
        'carpet_area':carpet_area
    }
    return render(request, 'summary.html',context) 

def ResultView(request):
    user = Home.objects.latest('submitted_at') 
    summary = Summary.objects.get(user_name=user) 


    WALLS_AREA = 150
    STAIRS_AREA = 200

    
    floor1_area = Room.objects.filter(user_name=user, floor_numm=1).aggregate(Sum('room_area'))['room_area__sum'] +  WALLS_AREA + STAIRS_AREA
    total_str_cost = (floor1_area + Summary.objects.get(user_name=user).total_house_area) * 1800
    total_room_cost = sum(room.cost for room in user.room.all()) if user.room.exists() else 0
    total_other_cost = sum(other.cost for other in user.other.all()) if user.other.exists() else 0
    total_cost = total_room_cost + total_other_cost
    noofffloors = Summary.objects.get(user_name=user).no_of_floors
    
    total_str_lab_cost = (floor1_area + Summary.objects.get(user_name=user).total_house_area) * 400
    total_paint_labor_cost =  noofffloors * 40000
    total_elec_labor_cost = noofffloors * 40000
    numberofbathrooms = Other.objects.filter(user_name=user, finish_type='bathroom').count()
    numberofkitchen = Other.objects.filter(user_name=user, finish_type='kitchen').count()
    total_sani_labor_cost = numberofbathrooms * 14000 + numberofkitchen * 10000
    construction_standard=user.construction_standard
    rate_per_squire_feet= (total_str_cost + total_cost) / summary.total_house_area

    context = {
        'summary': summary,
        'total_cost': total_cost,
        'current_year': datetime.datetime.now().year, 
        'total_str_cost':total_str_cost,
        'total_const_cost':total_str_cost + total_cost,
        'total_str_lab_cost': total_str_lab_cost,
        'total_paint_labor_cost':total_paint_labor_cost,
        'total_elec_labor_cost': total_elec_labor_cost,
        'total_sani_labor_cost':total_sani_labor_cost,        
        'construction_standard':construction_standard,        
        'rate_per_squire_feet':rate_per_squire_feet        
    }
    return render(request, 'result.html', context)



