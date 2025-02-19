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
    name = models.CharField(max_length=255)
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
    contact_number = models.CharField(max_length=13)
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
        ('dining', 'Dining'),
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
    
    user_name = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='room')
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES)
    quantity = models.PositiveIntegerField(default=0)
    flooring_type = models.CharField(max_length=50, choices=FLOORING_CHOICES, default='none')
    room_area = models.PositiveIntegerField(default=0)


    def save(self, *args, **kwargs):
        self.room_area = self.ROOM_AREAS.get(self.room_type, 0) * self.quantity
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
    
    user_name = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='other')
    compound_flooring = models.CharField(max_length=50, choices=MATERIAL_CHOICES, default='stone')
    staircase_flooring = models.CharField(max_length=50, choices=STAIRCASE_FLOORING_CHOICES, default='tile')
    window_type = models.CharField(max_length=50, choices=WINDOW_TYPES, default='upvc')
    
    def __str__(self):
        return f"Features for {self.user_name.name}"


class Summary(models.Model):
    
    WALLS_AREA = 150
    STAIRS_AREA = 200
    WALLS_AREA_SC_only = 50
    
    user_name = models.OneToOneField(Home, on_delete=models.CASCADE, related_name='summary')
    phone_number = models.CharField(max_length=13)
    total_house_area = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Summary for {self.user_name.name}"
    
    def save(self, *args, **kwargs):
        # Calculate total room area using the area field
        total_room_area = sum(room.room_area for room in self.user_name.room.all())
        
        floors = self.user_name.floor.all()
        num_floors = floors.count()
        
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


class Cost(models.Model):
    TOTAL_COST_DEFAULTS = {
        'affordable': {'tile': 280, 'granite': 550, 'parquet': 120},
        'premium': {'tile': 500, 'granite': 800, 'parquet': 300, 'sisou': 400}
    }
    
    user_name = models.OneToOneField(Home, on_delete=models.CASCADE, related_name='cost')
    phone_number = models.CharField(max_length=13)
    total_cost = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Cost for {self.user_name.name}"

    def save(self, *args, **kwargs):
        construction_standard = self.user_name.construction_standard
        cost_rates = self.TOTAL_COST_DEFAULTS.get(construction_standard, {})
        total_cost = 0
        
        for room in self.user_name.room.all():
            rate = cost_rates.get(room.flooring_type, 0)
            total_cost += rate * room.room_area  # Use room.area instead of room.room_area
            
        self.total_cost = total_cost
        
        location = Location.objects.filter(user_name=self.user_name).first()
        if location:
            self.phone_number = location.contact_number
            
        super().save(*args, **kwargs)
        
        


