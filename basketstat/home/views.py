from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
	return render(request, 'home/home.html')


def about(request):
	return render(request, 'home/about.html')


def test(request):
	context = {
		'a': 1,
		'b': 2,
		'c': 3
	}
	return render(request, 'home/test.html', context)






