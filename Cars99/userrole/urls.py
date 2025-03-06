from django.urls import path
from . views import Signup,user_login,user_logout,profile,verify_otp,update_profile

urlpatterns=[
    path('signup/',Signup,name='signup_url'),
    path('verify_otp/',verify_otp,name='verify_otp_url'),
    path('login/',user_login,name='login_url'),
    path('logout/',user_logout,name='logout_url'),
    path('profile/',profile,name='profile_url'),
    path("profile/update", update_profile, name="update_profile_url"),

]