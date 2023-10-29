from django import forms
from .models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = ['first_name', 'last_name', 'phone', 'avatar', 'country', 'birthdate', 'fb_account']
        fields = ['first_name', 'last_name', 'phone', 'avatar', 'country', 'fb_account']

    avatar = forms.ImageField(
        required=False,  # Allow clearing the avatar field
        widget=forms.FileInput(attrs={'accept': 'image/*'}),  # Allow only image files
    )
