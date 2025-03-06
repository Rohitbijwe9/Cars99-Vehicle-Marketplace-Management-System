from .models import Car,TestDriveBooking,Intrest
from django import forms
from datetime import date


class CarForm(forms.ModelForm):
    class Meta:
        model=Car
        exclude=exclude = ['seller', 'created_at','is_approved']  
    

class IntrestForm(forms.ModelForm):
    class Meta:
        model=Intrest
        exclude=['timestamp']




class TestDriveBookingForm(forms.ModelForm):
    """Form for booking a test drive"""

    class Meta:
        model = TestDriveBooking
        fields = ["location", "address", "date", "time_slot"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "time_slot": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "location": forms.Select(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean_date(self):
        """Ensure the selected date is not in the past"""
        selected_date = self.cleaned_data.get("date")
        if selected_date < date.today():
            raise forms.ValidationError("You cannot select a past date for the test drive.")
        return selected_date

    def clean_address(self):
        """Ensure address is provided if 'Home Test Drive' is selected"""
        location = self.cleaned_data.get("location")
        address = self.cleaned_data.get("address")

        if location == "home" and not address:
            raise forms.ValidationError("Please provide an address for a home test drive.")
        
        return address



