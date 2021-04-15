from django.shortcuts import render, redirect
from django.contrib import messages # for flashing messages

# import our self defined forms from forms.py
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

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




# user must be logged in to view this page
# specify the LOGIN_URL in settings.py
# the user Profile view
@login_required
def profile(request):
    if request.method == 'POST':
        # UserUpdateForm is a Model form
        # So to fill in the fields, we can just fill in the spaces
        # by specifying the original fields data
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES, # file data coming in with file upload
                                   instance=request.user.profile)
        # Check if valid, then save
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # redirect, so that we don't send a post again

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'usrs/profile.html', context)

