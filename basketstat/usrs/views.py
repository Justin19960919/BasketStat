from django.shortcuts import render, redirect
from django.contrib import messages # for flashing messages

# import our self defined forms from forms.py
from .forms import UserRegisterForm

# import a decorator to limit user access
from django.contrib.auth.decorators import login_required



# Create your views here.


def register(request):
	# request.method
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)	# create a form with the POSTed data
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"Your account has been created {username}!")
			return redirect('login')	# this name is defined in record/urls.py

	else:
		form = UserRegisterForm()	
	
	# pass in a dict to pass variables
	return render(request, 'usrs/register.html', {'form': form})
