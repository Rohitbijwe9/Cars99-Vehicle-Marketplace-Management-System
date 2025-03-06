from django.urls import path
from .views import CarView,SignupView,LoginView,LogoutView,ShowCar,verify_otp,show_interest,IntrestSuccess,MyInterestView,remove_interest,mylistings,editcar,deletecar,book_test_drive,test_drive_list,update_test_drive,cancel_test_drive


urlpatterns=[
    path('car/',CarView,name='car_url'),

    
    path('carshow/',ShowCar,name='showcar_url'),
    path('cars/<int:pk>/', ShowCar, name='car_detail'),
    path('car/<int:pk>/interest/', show_interest, name='show_interest'),
    path('caredit/<int:pk>/',editcar,name='editcar_url'),
    path('deletecar/<int:pk>/',deletecar,name='deletecar_url'),

    path('intrest_success/',IntrestSuccess,name='intrest_sucess_url'),
    path('myinterest/',MyInterestView,name='myinterest_url'),
    path('removeinterest/<int:pk>/',remove_interest,name='remove_intrest_url'),
    path('mylistings/',mylistings,name='mylistings_url'),

    path('booktestdrive/<int:car_id>/',book_test_drive,name='booktestdrive_url'),
    path('showtestdrive/',test_drive_list,name='testdrivelist_url'),
    path('updatetestdrive/<int:booking_id>/', update_test_drive, name='updatetestdrive_url'),
    path('canceltestdrive/<int:booking_id>/', cancel_test_drive, name='canceltestdrive_url'),
   


]



'''

    path('signup/',SignupView,name='signup_url'),
    path('verify_otp/',verify_otp,name='verify_otp_url'),
    path('login/',LoginView,name='login_url'),
    path('logout/',LogoutView,name='logout_url'),

'''
    