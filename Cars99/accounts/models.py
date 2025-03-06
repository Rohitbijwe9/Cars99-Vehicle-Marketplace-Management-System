from django.db import models
from django.contrib.auth.models import User
from Cars99 import settings
from django.conf import settings 
from django.core.exceptions import ValidationError



class Car(models.Model):
    BRAND_CHOICES = [
        ("Jaguar", "Jaguar"),
        ("BMW", "BMW"),
        ("Mercedes", "Mercedes"),
        ("Audi", "Audi"),
        ("Skoda", "Skoda"),
        ("Volkswagen", "Volkswagen"),
        ("Toyota", "Toyota"),
        ("Ford", "Ford"),
        ("Honda", "Honda"),
        ("Hyundai", "Hyundai"),
        ("Kia", "Kia"),
        ("Renault", "Renault"),
        ("MG", "MG"),
        ("Suzuki", "Suzuki"),
        ("Tata", "Tata"),
        ("Mahindra", "Mahindra"),
    ]
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, choices=BRAND_CHOICES)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='car/seller_car')
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  


    def __str__(self):
        return f"{self.brand} {self.name} - {self.seller.first_name} ({self.seller.email})"


class Intrest(models.Model):  
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="interests") 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')  # Prevent duplicate interests

    def __str__(self):
        return f"{self.user.first_name} is interested in {self.car.name}"  # FIX HERE
    
    


class TestDriveBooking(models.Model):
    LOCATION_CHOICES = [
        ('home', 'Home Test Drive'),
        ('center', 'Test Drive at Center'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="test_drives")
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    address = models.TextField(blank=True, null=True)  # Required only for "home" test drive
    date = models.DateField()
    time_slot = models.TimeField()
    status = models.CharField(max_length=15, default="Pending")

    def __str__(self):
        return f"{self.user.username} booked a {self.car.name} test drive on {self.date}"

    def clean(self):
        """ Ensure address is provided for home test drives """
        if self.location == "home" and not self.address:
            raise ValidationError({"address": "Address is required for a home test drive."})
