from django.db import models

class Home(models.Model):
    STATUS_CHOICES = [
        ('affordable', 'Affordable Construction'),
        ('premium', 'Premium Construction'),
    ]
    LAND_AREA_CHOICES = [
        ('2.5-3.0', '2.5 to 3.0 aana'),
        ('3.0-3.5', '3.0 to 3.5 aana'),
        ('3.5-4.0', '3.5 to 4.0 aana'),
        ('4.0-4.5', '4.0 to 4.5 aana'),
        ('4.5-5.0', '4.5 to 5.0 aana'),
        ('> 5.0', 'Greater than 5 aana'),
    ]
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    land_area = models.CharField(max_length=20, choices=LAND_AREA_CHOICES)
    ground_coverage = models.FloatField(max_length=50)
    construction_standard = models.CharField(max_length=20, choices=STATUS_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class District(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='municipalities')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
class Location(models.Model):
    user_name = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='locations')
    contact_number = models.CharField(max_length=13,unique=True, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.municipality.name
    

class Floor(models.Model):
    user_name = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='floor')
    floor_number = models.PositiveIntegerField()
    staircase = models.BooleanField(default=False)

    def __str__(self):
        return f"Floor {self.floor_number}"

class Room(models.Model):
    FLOORING_CHOICES = [
        ('none', 'None'),
        ('tile', 'Tile'),
        ('granite', 'Granite'),
        ('parquet', 'Parquet'),
        ('sisou', 'Sisou'),
    ]

    ROOM_TYPES = [
        ('bedroom', 'Bedroom'),
        ('living', 'Living'),
        ('kitchen', 'Kitchen'),
        ('bathroom', 'Bathroom'),
        ('parking', 'Parking'),
        ('puja', 'Puja Room'),
        ('laundry', 'Laundry Room'),
        ('store', 'Store Room'),
    ]
    
    ROOM_AREAS = {
        'bedroom': 100,
        'living': 100,
        'kitchen': 100,
        'bathroom': 30,
        'parking': 120,
        'puja': 50,
        'laundry': 25,
        'store': 25
    }
    WINDOW_AREAS_DEFAULT = {
        'bedroom': 30,
        'living': 30,
        'kitchen': 30,
        'bathroom': 6,
        'parking': 0,
        'puja': 6,
        'laundry': 6,
        'store': 6
    }
    
    TOTAL_COST_DEFAULTS = {
        'affordable': {'tile': 280, 'granite': 550, 'parquet': 120, 'sisou': 350, 'none': 50},
        'premium': {'tile': 500, 'granite': 800, 'parquet': 300, 'sisou': 450, 'none': 100}
    }
    
    user_name = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='room')
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms')
    floor_numm = models.PositiveIntegerField(default=0)
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES)
    quantity = models.PositiveIntegerField(default=0)
    flooring_type = models.CharField(max_length=50, choices=FLOORING_CHOICES, default='none')
    room_area = models.PositiveIntegerField(default=0)
    rate = models.PositiveIntegerField(default=0)
    cost = models.PositiveIntegerField(default=0)
    window_area =   models.PositiveIntegerField(default=0) 

    def save(self, *args, **kwargs):
        self.room_area = self.ROOM_AREAS.get(self.room_type, 0) * self.quantity
        self.rate = self.TOTAL_COST_DEFAULTS.get(self.user_name.construction_standard, {}).get(self.flooring_type, 0)
        self.cost = self.rate * self.room_area
        self.window_area = self.WINDOW_AREAS_DEFAULT.get(self.room_type, 0) * self.quantity
        super().save(*args, **kwargs)
        
               
    def __str__(self):
        return f"{self.room_type} - {self.floor} ({self.quantity})"

class Other(models.Model):
    MATERIAL_CHOICES = [
        ('stone', 'Stone'),
        ('block', 'Block'),
        ('tile', 'Tile'),
    ]
    
    STAIRCASE_FLOORING_CHOICES = [
        ('tile', 'Tile'),
        ('granite', 'Granite'),
        ('parquet', 'Parquet'),
        ('sisou', 'Sisou'),
    ]
    
    WINDOW_TYPES = [
        ('upvc', 'UPVC'),
        ('aluminum', 'Aluminum'),
        ('wood', 'Wood'),
    ]
    land_area_map = {
            '2.5-3.0': 3.0,
            '3.0-3.5': 3.5,
            '3.5-4.0': 4.0,
            '4.0-4.5': 4.5,
            '4.5-5.0': 5.0,
            '> 5.0': 20 
        }

    COSTS_DEFAULTS = {
        'staircase_flooring':{
            'affordable': {
                'tile': 350,
                'granite': 650,
                'parquet': 400,
                'sisou': 700
            },
            'premium': {
                'tile': 500,
                'granite': 800,
                'parquet': 600,
                'sisou': 1400
            }
        },
        'compound_flooring': {
            'affordable': {
                'tile': 580, # INCUDING PCC
                'block': 350,
                'stone': 450
            },
            'premium': {
                'tile': 800,
                'block': 500,
                'stone': 600
            }
        },
        'window_type': {
            'affordable': {
                'upvc': 650,
                'aluminum': 600,
                'wood': 1500
            },
            'premium': {
                'upvc': 1200,
                'aluminum': 900,
                'wood': 2200
            
            } 
        },
        'main_door': {
            'affordable': {
                'main_door': 50000
            },
            'premium': {
                'main_door': 200000,
            } 
        },
        'door': {
            'affordable': {
                'door': 18000
            },
            'premium': {
                'door': 25000,
            } 
        },
        'mod_kitchen': {
            'affordable': {
                'mod_kitchen': 250000
            },
            'premium': {
                'mod_kitchen': 600000,
            } 
        },
        'landscape': {
            'affordable': {
                'landscape': 150000
            },
            'premium': {
                'landscape': 500000,
            } 
        },
        'paint':{
            'affordable': {
                'paint': 100000,
            },
            'premium': {
                'paint': 250000,
            }
        },
        'electrical':{
            'affordable': {
                'electrical': 100000,
            },
            'premium': {
                'electrical': 250000,
            }
        },
        'plumbing':{
            'affordable': {
                'plumbing': 100000,
            },
            'premium': {
                'plumbing': 150000,
            }
        },
        'bathroom':{
            'affordable': {
                'bathroom': 40000,
            },
            'premium': {
                'bathroom': 120000,
            }
        },
        'kitchen':{
            'affordable': {
                'kitchen': 20000,
            },
            'premium': {
                'kitchen': 40000,
            }
        },
        'sani_other':{
            'affordable': {
                'sani_other': 50000,
            },
            'premium': {
                'sani_other': 200000,
            }
        },
        'railing':{
            'affordable': {
                'raling': 40000,
            },
            'premium': {
                'railing': 100000,
            }
        },
        'other_metal_works':{
            'affordable': {
                'other_metal_works': 100000,
            },
            'premium': {
                'other_metal_works': 200000,
            }
        },
        'misc':{
            'affordable': {
                'misc': 100000,
            },
            'premium': {
                'misc': 200000,
            }
        }
    }
    
 

    user_name = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='other')
    phone_number= models.CharField(max_length=13)
    finish_type= models.CharField(max_length=50) # window_type, compound_flooring, staircase_flooring
    finish= models.CharField(max_length=50)  # alumium, upvc, etc.. tile stone etc 
    qty= models.CharField(max_length=100)
    rate=models.PositiveIntegerField(default=0)
    cost=models.PositiveIntegerField(default=0)   
    
    
    
    def __str__(self):
        return f"Features for {self.user_name.name}"
    
    def save(self, *args, **kwargs):
        noofffloors = self.user_name.floor.all().count()
        user_gc = Home.objects.latest('submitted_at').ground_coverage
        COMPOUND_AREA = self.land_area_map[Home.objects.latest('submitted_at').land_area]*342.25-Home.objects.latest('submitted_at').ground_coverage
        STAIRS_AREA = (noofffloors - 1)* 80 + 25 * (2* (noofffloors - 1) + 1 )
        WINDOW_AREA = Room.objects.filter(user_name=self.user_name).aggregate(models.Sum('window_area'))['window_area__sum'] + (noofffloors * 9.5 * 4 ) -4 # 9.5 ft floor height / 4 ft width of window -4 ft for under staircase deduction
        numofroom=self.user_name.room.all().count()
        NUMBER_OF_DOORS = numofroom + 3
        numberofbathrooms = self.user_name.room.filter(room_type='bathroom').count()
        numberofkitchen = self.user_name.room.filter(room_type='kitchen').count()
        multiplier =  (user_gc + abs(1000 - user_gc) * user_gc/1000)/1000
        
        
        QTTY = {
            'compound_flooring':COMPOUND_AREA,
            'staircase_flooring':STAIRS_AREA,
            'window_type':WINDOW_AREA,
            'main_door':1,
            'door':NUMBER_OF_DOORS,
            'mod_kitchen':1,
            'sani_other':1,
            'landscape':1,
            'paint':noofffloors*multiplier,
            'electrical':noofffloors*multiplier,
            'plumbing':noofffloors*multiplier,
            'bathroom':numberofbathrooms,
            'kitchen':numberofkitchen,
            'railing':noofffloors*multiplier,
            'other_metal_works':1,
            'misc':1
            
        }
        self.qty = QTTY.get(self.finish_type, 0)
        self.rate = Other.COSTS_DEFAULTS.get(self.finish_type, 0).get(self.user_name.construction_standard, {}).get(self.finish, 0)
        self.cost = self.rate * self.qty
        super().save(*args, **kwargs)

class Summary(models.Model):
    
    WALLS_AREA = 150
    STAIRS_AREA = 200
    WALLS_AREA_SC_only = 50
    
    user_name = models.OneToOneField(Home, on_delete=models.CASCADE, related_name='summary')
    phone_number = models.CharField(max_length=13)
    total_house_area = models.PositiveIntegerField(default=0)
    no_of_floors = models.PositiveIntegerField(default=0)
    total_carpet_area = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Summary for {self.user_name.name}"
    
    def save(self, *args, **kwargs):
        # Calculate total room area using the area field
        total_room_area = sum(room.room_area for room in self.user_name.room.all())
        
        # Calculate total carpet area (sum of living room, bedroom, kitchen)
        carpet_room_types = ['bedroom', 'living', 'kitchen']
        self.total_carpet_area = sum(
            room.room_area for room in self.user_name.room.filter(room_type__in=carpet_room_types)
        )
        
        
        floors = self.user_name.floor.all()
        num_floors = floors.count()
        
        self.no_of_floors = num_floors
        
        has_staircase = floors.filter(staircase=True).exists()

        if has_staircase:
            self.total_house_area = (total_room_area + self.STAIRS_AREA * num_floors +
                                     self.WALLS_AREA_SC_only + self.WALLS_AREA * (num_floors - 1))
        else:
            self.total_house_area = (total_room_area + (self.WALLS_AREA + self.STAIRS_AREA) * num_floors)
        
        location = Location.objects.filter(user_name=self.user_name).first()
        if location:
            self.phone_number = location.contact_number 
        
        super().save(*args, **kwargs)



    
        


