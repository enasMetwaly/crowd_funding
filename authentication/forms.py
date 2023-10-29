from .models import *
from django.contrib.auth.forms import *


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser



class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        #help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label="Password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Enter the same password as before, for verification.",
    )


    phone = forms.CharField(
        label="Phone",
        required=False,
    )

    profile_image = forms.ImageField(
        label="Profile Image",
        required=True,
    )

    class Meta:
        model = get_user_model()  # Use the custom user model
        fields = ['first_name', 'last_name', 'email','phone']

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     User = get_user_model()
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError('A user with this email already exists.')
    #     return email


    def clean_password1(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        # Validate the password
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error('password1', error)

        return password1

    # Validate the passwords matching
    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        # Check if the passwords are identical
        if password1 != password2:
            self.add_error('password2', "Passwords don't match")
        return password2



    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True  # Wait for confirmation email

        if commit:
            user.save()
        return user

class LoginForm (AuthenticationForm):

    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))

    error_messages = {

        'invalid_login':"Invalid Email or password.",

        'inactive':"Please confirm your email.",
    }


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)


