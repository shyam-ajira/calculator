from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from .forms import *
import datetime
from django.db.models import Sum
import random
from .utils import send_sms
from django.conf import settings
import re


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


def is_valid_number(number):
    return bool(re.fullmatch(r"9[78]\d{8}", number))

def generate_otp():
    return str(random.randint(100000, 999999))

def LocationView(request):
    districts = District.objects.all()
    user_name = Home.objects.latest('submitted_at')

    # Step tracking
    step = request.session.get("step", 1)

    if request.method == "POST":
        if step == 1:
            contact_number = request.POST.get("contact_number")
            otp_input = request.POST.get("otp")

            # If OTP is not submitted yet → send it
            if not otp_input:
                if not is_valid_number(contact_number):
                    messages.error(request, "Invalid phone number.")
                    return render(request, "location.html", {"step": 1})

                otp = generate_otp()
                request.session["otp"] = otp
                request.session["contact_number"] = contact_number

                result = send_sms(contact_number, f"Your OTP for Ajira Builders is: {otp}", settings.SMS_AUTH_TOKEN)
                if result["status_code"] != 200:
                    messages.error(request, "Failed to send OTP.")
                    return render(request, "location.html", {"step": 1})

                messages.success(request, "OTP sent successfully.")
                return render(request, "location.html", {"step": 1, "show_otp": True})

            else:
                # Verify OTP
                if otp_input != request.session.get("otp"):
                    messages.error(request, "Incorrect OTP. Try again.")
                    return render(request, "location.html", {"step": 1, "show_otp": True})

                # OTP verified → move to step 2
                request.session["step"] = 2
                messages.success(request, "OTP verified.")
                return redirect("location")

        elif step == 2:
            district_id = request.POST.get("district")
            municipality_id = request.POST.get("local-body")
            contact_number = request.session.get("contact_number")

            if not (district_id and municipality_id and contact_number):
                messages.error(request, "All fields are required.")
                return render(request, "location.html", {"step": 2, "districts": districts})

            district = District.objects.get(id=district_id)
            municipality = Municipality.objects.get(id=municipality_id)
            if Location.objects.filter(contact_number=contact_number).exists():
                messages.error(request, "This contact number has already been used.")
                return render(request, "location.html", {
                    "step": 2,
                    "districts": districts
                })

            Location.objects.create(
                user_name=user_name,
                contact_number=contact_number,
                district=district,
                municipality=municipality
            )

            # Clear session
            request.session.flush()
            messages.success(request, "Location saved successfully.")
            return redirect("flooring")

    return render(request, "location.html", {
        "step": step,
        "districts": districts if step == 2 else None
    })


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



def report(request, user_id):
    user_home = get_object_or_404(Home, id=user_id)
    location = Location.objects.filter(user_name=user_home).first()
    floors = Floor.objects.filter(user_name=user_home)
    rooms = Room.objects.filter(user_name=user_home)
    others = Other.objects.filter(user_name=user_home)
    summary = Summary.objects.filter(user_name=user_home).first()
    has_staircase = any(floor.staircase for floor in floors)


    # Constants
    WALLS_AREA = 150
    STAIRS_AREA = 200

    # Floor 1 Area Calculation
    floor1_area = Room.objects.filter(user_name=user_home, floor_numm=1).aggregate(Sum('room_area'))['room_area__sum'] or 0
    floor1_area += WALLS_AREA + STAIRS_AREA

    # Cost Calculations
    total_str_cost = (floor1_area + summary.total_house_area) * 1800 if summary else 0
    total_room_cost = sum(room.cost for room in rooms) if rooms else 0
    total_other_cost = sum(other.cost for other in others) if others else 0
    total_cost = total_room_cost + total_other_cost
    no_of_floors = summary.no_of_floors if summary else 1

    # Labor Costs
    total_str_lab_cost = (floor1_area + summary.total_house_area) * 400 if summary else 0
    total_paint_labor_cost = no_of_floors * 40000
    total_elec_labor_cost = no_of_floors * 40000
    number_of_bathrooms = Other.objects.filter(user_name=user_home, finish_type='bathroom').count()
    number_of_kitchen = Other.objects.filter(user_name=user_home, finish_type='kitchen').count()
    total_sani_labor_cost = number_of_bathrooms * 14000 + number_of_kitchen * 10000
    construction_standard = user_home.construction_standard
    rate_per_square_feet = (total_str_cost + total_cost) / summary.total_house_area if summary else 0

    context = {
        'user_home': user_home,
        'location': location,
        'floors': floors,
        'has_staircase': has_staircase,
        'rooms': rooms,
        'others': others,
        'summary': summary,
        'total_cost': total_cost,
        'current_year': datetime.datetime.now().year, 
        'total_str_cost': total_str_cost,
        'total_const_cost': total_str_cost + total_cost,
        'total_str_lab_cost': total_str_lab_cost,
        'total_paint_labor_cost': total_paint_labor_cost,
        'total_elec_labor_cost': total_elec_labor_cost,
        'total_sani_labor_cost': total_sani_labor_cost,        
        'construction_standard': construction_standard,        
        'rate_per_square_feet': rate_per_square_feet        
    }

    return render(request, 'report.html', context)