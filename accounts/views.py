from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random

from .models import OTP


#  REGISTER
def register(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        #  Validation
        if not username or not email or not password:
            messages.error(request, "All fields are required")
            return redirect('accounts:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('accounts:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('accounts:register')

        # ✅ Create user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully")

        return redirect('login')

    return render(request, 'accounts/register.html')


#  FORGOT PASSWORD 
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()

        users = User.objects.filter(email=email)

        if not users.exists():
            messages.error(request, "Email not found")
            return redirect('accounts:forgot_password')

        
        user = users.first()

        otp = str(random.randint(100000, 999999))

        # 🧹 Delete old OTP
        OTP.objects.filter(user=user).delete()

        OTP.objects.create(user=user, otp=otp)

        #  Send email
        send_mail(
            'Password Reset OTP',
            f'Your OTP is {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False
        )

        request.session['email'] = email

        return redirect('accounts:verify_otp')

    return render(request, 'accounts/forgot_password.html')


#  VERIFY OTP
def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        email = request.session.get('email')

        if not email:
            messages.error(request, "Session expired")
            return redirect('accounts:forgot_password')

        users = User.objects.filter(email=email)

        if not users.exists():
            return redirect('accounts:forgot_password')

        user = users.first()

        otp_obj = OTP.objects.filter(user=user).last()

        if otp_obj and otp_obj.otp == entered_otp:
            return redirect('accounts:reset_password')
        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'accounts/verify_otp.html')


#  RESET PASSWORD
def reset_password(request):
    if request.method == "POST":
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect('accounts:reset_password')

        email = request.session.get('email')

        if not email:
            messages.error(request, "Session expired")
            return redirect('accounts:forgot_password')

        users = User.objects.filter(email=email)

        if not users.exists():
            return redirect('accounts:forgot_password')

        user = users.first()

        #  Update password
        user.set_password(password)
        user.save()

        # 🧹 Cleanup
        OTP.objects.filter(user=user).delete()
        request.session.flush()

        messages.success(request, "Password updated successfully")

        return redirect('login')

    return render(request, 'accounts/reset_password.html')