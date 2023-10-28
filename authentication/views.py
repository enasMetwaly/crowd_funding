from django.shortcuts import render,redirect,reverse




from django.shortcuts import render ,reverse
from django.urls import reverse_lazy
from django.shortcuts import *
from django.utils.encoding import force_str

from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
# Create your views here.
from .token import \
    AccountActivationTokenGenerator as TokenGenerator, AccountActivationTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from user.models import User, UserProfile

from .forms import LoginForm, RegisterForm

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect

from social_django.models import UserSocialAuth
from .models import CustomUser  # Import your CustomUser model from the appropriate location

from django.urls import reverse  # If you need to work with URL reversing
from django.http import HttpResponse  # For returning HTTP responses

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from django.contrib.auth import login  # If you need to log in users

# Import your token generator if not already done
from .token import AccountActivationTokenGenerator
from django.contrib.auth import login as auth_login  # Import Django's login function with an alias

account_activation_token = AccountActivationTokenGenerator()


class SettingsView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user

        try:
            facebook_login = user.social_auth.get(provider='facebook')
        except UserSocialAuth.DoesNotExist:
            facebook_login = None

        can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

        return render(request, 'authentication/setting.html', {
            'facebook_login': facebook_login,
            'can_disconnect': can_disconnect
        })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'authentication/password.html', {'form': form})




# class HomeView(LoginRequiredMixin, TemplateView):
#     template_name = "social_login.html"

def home(request):
    return render(request,'index.html',context={})



# def register(request):
#     form = RegisterForm(request.POST or None)
#     if request.method == 'POST':
#         user_profile = UserProfile.objects.get(user=request.user)
#
#         # Handle file upload
#         uploaded_image = request.FILES['avatar']
#         if uploaded_image:
#             user_profile.avatar.save(
#                 uploaded_image.name,
#                 ContentFile(uploaded_image.read())
#             )
#             user_profile.save()
#
#     if form.is_valid():
#         user = form.save()
#         UserProfile.objects.create(user_id=user.id, avatar=user.avatar)
#         #send activation mail
#         send_activation_email(request, form.cleaned_data.get('email'), user)
#
#         return redirect("login")
#     else:
#         print(form.errors)  # Debug: Print form errors to the console
#
#     return render(request, "authentication/register.html", {"form": form})
from django.core.files.base import ContentFile

# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#
#             # Handle file upload
#             uploaded_image = request.FILES.get('profile_image')
#             if uploaded_image:
#                 user_profile, created = UserProfile.objects.get_or_create(user=user)
#                 user_profile.avatar.save(
#                     uploaded_image.name,
#                     ContentFile(uploaded_image.read())
#                 )
#                 user_profile.save()
#
#                 # Send activation email and redirect to login or another page
#                 send_activation_email(request, form.cleaned_data.get('email'), user)
#
#             return render(request, "authentication/registeration/login.html", {"form": form})
#     else:
#         form = RegisterForm()
#
#     return render(request, "authentication/register.html", {"form": form})

#
from django.core.files.base import ContentFile

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Handle file upload
            uploaded_image = request.FILES.get('profile_image')
            if uploaded_image:
                user_profile, created = UserProfile.objects.get_or_create(user=user)
                user_profile.avatar.save(
                    uploaded_image.name,
                    ContentFile(uploaded_image.read())
                )
                user_profile.save()

                # Send activation email and redirect to login or another page
                send_activation_email(request, form.cleaned_data.get('email'), user)

            return render(request, "authentication/login.html", {"form": form})
    else:
        form = RegisterForm()

    return render(request, "authentication/register.html", {"form": form})



def login(request):
    form = LoginForm(data=request.POST or None)
    if form.is_valid():
        auth_login(request, form.user_cache)  # Use the alias to call Django's login function
        return redirect("home")
    return render(request, "authentication/login.html", {"form": form})

def Logout(req):
    req.session.clear()
    return redirect(reverse('login'))


# def activate(request, uidb64, token):
#
#     # Decode the token
#     uid = urlsafe_base64_decode(uidb64).decode()
#     user = User.objects.get(pk=uid)
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     # Check if user is found and decoding is done
#     if user and activation_token.check_token(user, token):
#         # Activate the user
#         user.is_active = True
#         user.save()
#         # TODO: Activation is done
#         return redirect("login")
#
#     # TODO: Activation link is invalid
#     else:
#         return redirect("login")
#
#     # Send email confirmation

# account_activation_token = AccountActivationTokenGenerator()


# Create token object
activation_token = TokenGenerator()


def activate(request, uidb64, token):
    # Decode the token
    uid = urlsafe_base64_decode(uidb64)
    try:
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        # Activate the user
        user.is_active = True
        user.save()
        # TODO: Activation is done, you can redirect to a success page
        return redirect("home")

    # TODO: Activation link is invalid, you can redirect to an error page
    return redirect("login")

# Helpers

def send_activation_email(request, receiver_email, user):
    current_site = get_current_site(request)
    mail_subject = 'Account Activation'

    # Construct the email

    body = render_to_string('authentication/registeration/email_activation.html', {

        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': activation_token.make_token(user),
    })

    email = EmailMessage(
        mail_subject, body, to=[receiver_email]
    )

    # send the email
    email.send()


def _redirect(request, url):

    nxt = request.GET.get("next", None)
    if nxt:
        return redirect(nxt)

    else:
        return redirect(url)
