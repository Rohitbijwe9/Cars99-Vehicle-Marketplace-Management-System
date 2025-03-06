from django.shortcuts import render,redirect,get_object_or_404
from .forms import CarForm,IntrestForm,TestDriveBookingForm
from .models import Car,Intrest,TestDriveBooking
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import date





def SignupView(request):

    template_name = 'accounts/Signup.html'
    
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request,'Email already use, Please use diff email.')
        
        else:
            otp=random.randint(100000,999999)
            request.session['otp'] = otp
            request.session['signup_data'] = {
                'username': username,
                'email': email,
                'password': password
            }
             
            subject = 'Welcome to Cars99'
            message = f'Dear {username},\n\nWelcome to Cars99 registration.\nYour OTP is: {otp}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, 'OTP sent to your email. Please verify.')
            return redirect('verify_otp_url')


    return render(request, template_name)



def verify_otp(request):
    template_name = 'accounts/verifyotp.html'
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        if stored_otp and entered_otp and int(entered_otp) == stored_otp:
            user_data = request.session.get('signup_data')
            if user_data:
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password']
                )
                user.is_superuser = True  
                user.is_staff = True      
                user.save()

                messages.success(request, "Account verified successfully! Please log in.")

                del request.session['otp']
                del request.session['signup_data']

                return redirect('login_url')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, template_name)


def LoginView(request):
    template_name = 'accounts/Login.html'

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)  
        except User.DoesNotExist:
            user = None

        if user:
            print("User found:", user.username)  

            user = authenticate(request, username=user.username, password=password)  

            if user:
                print("Authentication successful!")  
                login(request, user)
                return redirect('home_url')
            else:
                messages.error(request, "Invalid email or password. Please try again.")
        else:
            messages.error(request, "Email not found. Please register first.")

    return render(request, template_name)

def LogoutView(request):
    logout(request)
    return redirect('login_url')




@login_required(login_url='login_url')
def CarView(request):
    template_name = 'accounts/CarForm.html'
    form = CarForm()

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)  
        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user
            car.is_approved = False  
            car.save()
            return redirect('showcar_url')  

    context = {'form': form}
    return render(request, template_name, context)


def ShowCar(request, pk=None):
    if pk:
        template_name='accounts/CarDetail.html'
        car = get_object_or_404(Car, id=pk)

        interest_count = Intrest.objects.filter(car=car).count()

        user_has_shown_interest = request.user.is_authenticated and Intrest.objects.filter(car=car, user=request.user).exists()

        return render(request, template_name, {
            'car': car,
            'interest_count': interest_count,  
            'user_has_shown_interest': user_has_shown_interest
        })
    else:
        cars = Car.objects.filter(is_approved=True)  
        template_name='accounts/Carshow.html'
        context={'cars': cars}

        return render(request,template_name,context )


def editcar(request, pk):
    template_name = 'accounts/editcar.html'
    car = get_object_or_404(Car, id=pk)  
    form = CarForm(instance=car)  

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user  
            car.is_approved = False  
            car.save()
            return redirect('showcar_url')  
    context = {'form': form, 'car': car}
    return render(request, template_name, context)


def deletecar(request,pk):
    car = get_object_or_404(Car, id=pk)  
    car.delete()
    return redirect('mylistings_url')






@login_required
def show_interest(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to show interest.")
        return redirect('login_url')

    car = get_object_or_404(Car, id=pk)

    if not Intrest.objects.filter(user=request.user, car=car).exists():
        Intrest.objects.create(user=request.user, car=car)

        email = request.user.email
        if email:
            subject = "Interest in Car - Cars99"
            user_name = request.user.first_name or request.user.email  
            message = f"Dear {user_name},\n\nThank you for showing interest in {car.brand} {car.name}. Our team will contact you soon.\n\nBest Regards,\nCars99 Team"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)

        return redirect('intrest_sucess_url')

    messages.info(request, "You have already shown interest in this car.")
    return redirect('car_details_url', pk=pk)


def MyInterestView(request):
    template_name='accounts/Myinterest.html'
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view your interests.")
        return redirect('login_url')
    else:
        interests = Intrest.objects.filter(user=request.user).select_related('car')
        context={'interests':interests}

    return render(request,template_name,context)



def remove_interest(request, pk):
    interest = get_object_or_404(Intrest, car_id=pk, user=request.user)
    interest.delete()
    messages.success(request, "Interest removed successfully.")
    return redirect('myinterest_url')





def IntrestSuccess(request):
    template_name='accounts/Intrestsuccess.html'
    return render(request,template_name)



def mylistings(request):
    template_name='accounts/mylistings.html'
    mycar=Car.objects.filter(seller=request.user)
    context={'mycars':mycar}
    return render(request,template_name,context)





@login_required
def book_test_drive(request, car_id):
    """ Allows logged-in users to book a test drive for a specific car """
    car = get_object_or_404(Car, id=car_id)  
    template_name = "accounts/book_test_drive.html"

    if request.method == "POST":
        form = TestDriveBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car  
            booking.save()
            messages.success(request, "Your test drive has been booked successfully!")
            return redirect("testdrivelist_url")  
    else:
        form = TestDriveBookingForm()

    return render(request, template_name, {"form": form, "car": car})




@login_required
def test_drive_list(request):
    """ Shows a list of test drives booked by the logged-in user """
    template_name='accounts/testdrivelist.html'
    bookings = TestDriveBooking.objects.filter(user=request.user).order_by("-date")
    context={'bookings':bookings}

    return render(request,template_name,context)



@login_required
def update_test_drive(request, booking_id):
    """ Allows users to update their test drive details before the scheduled date """
    booking = get_object_or_404(TestDriveBooking, id=booking_id, user=request.user)
    template_name='accounts/updatetestdrive.html'

    if request.method == "POST":
        form = TestDriveBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Your test drive details have been updated!")
            return redirect("testdrivelist_url")
    else:
        form = TestDriveBookingForm(instance=booking)
    context={'form':form,'booking':booking}

    return render(request,template_name,context)




@login_required
def cancel_test_drive(request, booking_id):
    """ Allows users to cancel a test drive before the scheduled date """
    booking = get_object_or_404(TestDriveBooking, id=booking_id, user=request.user)

    if booking.status == "Completed":
        messages.error(request, "You cannot cancel a completed test drive.")
    else:
        booking.delete()
        messages.success(request, "Your test drive has been canceled.")

    return redirect("testdrivelist_url")


