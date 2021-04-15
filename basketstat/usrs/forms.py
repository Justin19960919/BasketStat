from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm	# import User Creation Form to inherit

# import Profile mode
from .models import Profile


class UserRegisterForm(UserCreationForm):
	
	email = forms.EmailField()
	class Meta:
		model = User
		# define all fields (including additional)
		fields = ['username', 'email', 'password1', 'password2']



# form to update user and profile
# ModelForm: a form that interacts with a db model
class UserUpdateForm(forms.ModelForm):
	
	email = forms.EmailField()
	class Meta:
		model = User
		# define all fields (including additional)
		fields = ['username', 'email']



class ProfileUpdateForm(forms.ModelForm):
	
	class Meta:
		model = Profile
		fields = ['image']

