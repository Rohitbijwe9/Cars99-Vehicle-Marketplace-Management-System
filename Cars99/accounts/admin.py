from django.contrib import admin
from .models import Car, Intrest,TestDriveBooking
from django.core.mail import send_mail
from django.conf import settings
from django import forms
from .models import TestDriveBooking
from datetime import date

class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name', 'year', 'price', 'is_approved', 'seller')
    list_filter = ('is_approved',)
    search_fields = ('brand', 'name', 'seller__username')
    actions = ['approve_selected']

    def approve_selected(self, request, queryset):
        approved_cars = queryset.filter(is_approved=False)  # Only approve pending cars
        approved_cars.update(is_approved=True)  # Mark as approved
        
        # ✅ Send Email Notification to Seller
        for car in approved_cars:
            if car.seller and car.seller.email:  # Ensure seller has an email
                subject = "Car Listing Approved - Cars99"
                message = f"Dear {car.seller.username},\n\nYour car ({car.brand} {car.name}) has been approved and is now live on Cars99.\n\nBest Regards,\nCars99 Team"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [car.seller.email]

                send_mail(subject, message, from_email, recipient_list)

        self.message_user(request, "Selected cars have been approved and emails sent to sellers.")

    approve_selected.short_description = "Approve selected cars"

admin.site.register(Car, CarAdmin)
admin.site.register(Intrest)
admin.site.register(TestDriveBooking)

