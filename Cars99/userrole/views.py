from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout,get_backends
from django.http import JsonResponse
from .models import User,UserProfile
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserProfileForm





def Signup(request):
    template_name = 'CustomUser/Signup.html'

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        c_password = request.POST.get("c_password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        role = request.POST.get("role", "2")  

        if password != c_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup_url')

        if User.objects.filter(email=email).exists():
            messages.error(request, "User with this email already exists.")
            return redirect('signup_url')

        if role not in ["1", "2"]:  
            messages.error(request, "Invalid role selection.")
            return redirect('signup_url')

        otp = random.randint(100000, 999999)
        request.session['otp'] = otp
        request.session['signup_data'] = {
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'role': int(role),
        }

        subject = 'Cars99 - Email Verification OTP'
        message = f'Dear {first_name},\n\nYour OTP for Cars99 registration is: {otp}\n\nThank you!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, "OTP sent to your email. Please verify.")
        return redirect('verify_otp_url')

    return render(request, template_name)



def verify_otp(request):
    template_name = 'accounts/verifyotp.html'

    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        signup_data = request.session.get('signup_data')

        if not signup_data:
            messages.error(request, "Session expired, please sign up again.")
            return redirect('signup')

        if str(entered_otp) == str(stored_otp):
            user = User.objects.create_user(
                email=signup_data['email'],
                password=signup_data['password'],
                first_name=signup_data['first_name'],
                last_name=signup_data['last_name'],
                role=signup_data['role']
            )

            del request.session['otp']
            del request.session['signup_data']

            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login_url')

        else:
            messages.error(request, "Invalid OTP, please try again.")
            return redirect('signup_url')

    return render(request, template_name)



def user_login(request):
    template_name = 'CustomUser/Login.html'

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_superuser:
                messages.error(request, "Admins must log in via the admin panel.")
                return redirect("admin:login")  

            request.session.flush()  
            login(request, user)  
            request.session.set_expiry(86400)  
            messages.success(request, "Logged in successfully!")
            return redirect("home_url")

        messages.error(request, "Invalid email or password.")
        return redirect("login_url")

    return render(request, template_name)

def user_logout(request):
    logout(request)  
    messages.success(request, "Logged out successfully!")
    return redirect("login_url")  

def admin_logout(request):
    logout(request)  
    messages.success(request, "Admin logged out successfully!")
    return redirect("admin:login")  






@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    template_name = "accounts/User_Profile.html"
    if request.method=='POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_url')
    
    try:
        user = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found! Please complete your profile.")
        return render(request, template_name, {'user': None})  
    
    context = {'user': user}
    return render(request, template_name, context)




@login_required
def update_profile(request):
    template_name="CustomUser/update_profile.html"
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile_url")  
    else:
        form = UserProfileForm(instance=user_profile)
    context={'form':form}

    return render(request,template_name,context)