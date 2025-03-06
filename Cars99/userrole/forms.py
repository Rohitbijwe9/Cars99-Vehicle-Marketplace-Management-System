from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User,UserProfile

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "role"]

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "role"]
    
class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'profile_picture', 'gender', 'date_of_birth']
