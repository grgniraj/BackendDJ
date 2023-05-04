from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# Create your views here.


def signaction(request):
    if request.method == "POST":
        password = request.POST['password']
        try:
            validate_password(password)
        except ValidationError as e:
            # The password entered by the user is invalid
            # Handle the error here
            error_message = "Invalid password. Your password must contain at least 8 characters and should contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
            context = {'error_message': error_message}
            return render(request, 'signup_page.html', context)
        else:
            context = {}
            # The password entered by the user is valid
            # Process the data here
            # Get the form data from the request
            full_name = request.POST['fullname']
            email = request.POST['email']

            cpassword = request.POST['cpassword']
            if cpassword.__eq__(password):
                # Create a new ImsAdmin instance with the form data
                hashed_password = make_password(password)
                admin = User(username=full_name, email=email,
                              password=hashed_password, is_staff=True)

            # Save the new instance to the database
                status = admin.save()
                return render(request, 'signup_page.html', context)
            else:
                error_message = "Password Mismatch!!"
                context = {'error_message': error_message}
                return render(request, 'signup_page.html', context)
    else:
        context = {}
        return render(request, 'signup_page.html', context)


def homeaction(request):
    return render(request, 'Home.html')


def aboutaction(request):
    return render(request, 'aboutus.html')



@login_required
def dashboardaction(request):
    return render(request, 'Dash.html')

@login_required
def inventorytrackaction(request):
    return render(request, 'inventory_track.html')


@login_required
def changeaction(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Updating the session after a password change, logging out all other sessions
            # for security reasons, since the old password is no longer valid.
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

#for sending otp

import random
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

@login_required
def forgetaction(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Generate a random 6-digit OTP
            otp = str(random.randint(100000, 999999))
            # Compose the email message
            subject = 'Your OTP for password reset'
            message = f'Your OTP is {otp}.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            # Send the email using Gmail
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
            # Store the OTP in the session for later verification
            request.session['otp'] = otp
            # Render the verification page
            return render(request, 'verifyotp.html')
        else:
            error_message = 'Please enter a valid email address.'
            return render(request, 'forgotpass.html', {'error_message': error_message})
    else:
        return render(request, 'forgotpass.html')