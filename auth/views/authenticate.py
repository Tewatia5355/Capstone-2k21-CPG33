from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from eng import settings
from ..tokens import generate_token
from ..decorators import login_excluded


# Create your views here.
def home(request):
    return render(request, "auth/index.html")


@login_excluded("home")
def signup(request):
    if request.method == "POST":
        name = request.POST["nam"]
        email = request.POST["email"]
        password = request.POST["pass"]
        age = request.POST["age"]
        gender = request.POST["gender"]
        if gender == "Male":
            age_gender_data = str(age) + ",Male"
        elif gender == "Female":
            age_gender_data = str(age) + ",Female"
        else:
            age_gender_data = str(age) + ",Unknown"

        if User.objects.filter(username=email):
            messages.error(request, "User already exist with same email!")
            return redirect("home")

        if not (name.replace(" ", "")).isalpha():
            messages.error(request, "Name should consist of Alphabets only!")
            return redirect("home")

        myuser = User.objects.create_user(email, email, password)
        myuser.first_name = name
        myuser.last_name = age_gender_data
        myuser.is_active = False
        myuser.save()

        messages.success(request, "Your Account has been successfully created!")

        # Welcome Email
        subject = "Welcome to - Capstone CPG 33, 2k21"
        message = (
            "Hello "
            + myuser.first_name
            + "!!\nWelcome to Capstone CPG - 33\nThank you for visiting our Website\nA confirmation mail has been sent to you, please confirm you email\n\nThank You\n Capstone CPG 33"
        )
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Confirmation
        current_site = get_current_site(request)
        email_subject = "Confirm Email - Capstone CPG 33, 2k21 "
        message2 = render_to_string(
            "email_confirmation.html",
            {
                "name": myuser.first_name,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(myuser.pk)),
                "token": generate_token.make_token(myuser),
            },
        )
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()
        messages.success(request, "Confirm your Email-ID to Login")
        return redirect("home")
    return render(request, "auth/signup.html")


@login_excluded("home")
def signin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["pass"]
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile")
        else:
            messages.error(request, "Bad Credentials")
            return redirect("home")

    return render(request, "auth/login.html")


@login_required(login_url="login")
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Succesfully!")
    return redirect("home")


@login_excluded("home")
def activate(request, uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect("profile")
    else:
        return render(request, "activation_failed.html")


@login_required(login_url="login")
def prof(request):
    Role = (request.user.last_name).split(",")
    age = int(Role[0])
    gender = Role[1]
    return render(
        request,
        "auth/home.html",
        context={"Name": request.user.first_name, "age": age, "gender": gender},
    )
