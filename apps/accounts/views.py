from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import User, Destination, Joined
from django.contrib import messages

def index(request):
	return render(request, 'accounts/index.html')

def register(request):
	try:
		request.session['logged_in']
		return redirect(reverse('accounts_wall', kwargs={'id':request.session['logged_in']}))
	except KeyError:
		if User.userManager.register(request.POST, request):
			passFlag = True
			return redirect(reverse('accounts_index'))
		else:
			passFlag = False
			return redirect(reverse('accounts_index'))

def signin(request):
	if User.userManager.login(request.POST, request):
		passFlag = True
		username = request.POST['username']
		request.session['logged_in'] =  User.objects.get(username=username).id
		return redirect(reverse('accounts_travels', kwargs={'id':request.session['logged_in']}))
	else:
		return redirect(reverse('accounts_index'))

def travels(request, id):
	logged_in = request.session['logged_in']
	context = {
		"person": User.objects.get(id=id),
		"users": User.objects.all,
		"otherusers": User.objects.exclude(id=id),
		"destinations": Destination.objects.all,
		"joined": Joined.objects.all
	}
	return render(request, 'accounts/travels.html', context)

def addTripPage(request, id):
	logged_in = request.session['logged_in']
	context = {
		"person": User.objects.get(id=id)
	}
	return render(request, 'accounts/addTrip.html', context)

def addTrip(request):
	logged_in = request.session['logged_in']
	user = User.objects.get(id=request.session['logged_in'])
	if Destination.tripManager.register(request.POST, request):
		passFlag = True
		Destination.objects.create(planned_by_id=user, title=request.POST['title'], description=request.POST['description'], travelDateFrom=request.POST['travelDateFrom'], travelDateTo=request.POST['travelDateTo'])
		return redirect(reverse('accounts_travels', kwargs={'id':request.session['logged_in']}))
	else:
		passFlag = False
		return redirect(reverse('accounts_addTripPage'), user)

def logout(request):
	request.session.clear()
	return redirect (reverse('accounts_index'))

def destinationPage(request, destination):
	logged_in = request.session['logged_in']
	context = {
		"users": User.objects.all,
		"destinations": Destination.objects.all,
		"joined": Joined.objects.all
	}
	return render(request, 'accounts/destinationPage.html', context)