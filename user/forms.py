from django import forms
from .models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = ['first_name', 'last_name', 'phone', 'avatar', 'country', 'birthdate', 'fb_account']
        fields = ['first_name', 'last_name', 'phone', 'avatar', 'country', 'fb_account']

