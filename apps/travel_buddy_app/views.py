from django.shortcuts import render, redirect, HttpResponse
from .models import User, Trip
from django.db.models import Count
from django.contrib import messages
import bcrypt
  
def index(request):
  
	

	return render(request, 'travel_buddy_app/index.html')

def travels(request):
	if 'user_id' in request.session:
		user = currentUser(request)

		context = {
		"user": user,
		'trips': Trip.objects.all()
		}

	return render(request, 'travel_buddy_app/travels.html', context)

def addTrip(request):
	if 'user_id' in request.session:
		user = currentUser(request)

		context = {
		'user': user
		}


	return render(request, 'travel_buddy_app/addTrip.html', context)

def submitTrip(request):
	if request.method == 'POST':
		user = currentUser(request)

		trip = Trip.objects.create(destination=request.POST['destination'], plan=request.POST['description'], start_date=request.POST['from'], end_date=request.POST['end'], user=user)

		return redirect('/travels')

# def joinTrip(request, id):
# 	# if 'user_id' in request.session:
# 	# 	user = currentUser(request)

# 	# 	trip = Trip.objects.get(id=id)


# 	# 	trip.add(str(user))

# 		return redirect('/travels')

def destination(request, id):
	if 'user_id' in request.session:
		user = currentUser(request)


		context = {
		'user': user,
		'trip': Trip.objects.get(id=id),
		'trips': Trip.objects.all()
		}

		return render(request, 'travel_buddy_app/destination.html', context)

def currentUser(request):		
	user = User.objects.get(id=request.session['user_id'])

	return user

def register(request):
	if request.method == 'POST':
		
		errors = User.objects.validateRegistration(request.POST)

		if not errors:
			user = User.objects.createUser(request.POST)

			request.session['user_id'] = user.id

			return redirect('/travels')

		for error in errors:
			messages.error(request, error)
		print errors

	return redirect('/')

def login(request):
	if request.method == 'POST':
		errors = User.objects.validateLogin(request.POST)

		if not errors:
			user = User.objects.filter(email = request.POST['email']).first()

			if user:
				password = str(request.POST['password'])
				user_password = str(user.password)

				hashed_pw = bcrypt.hashpw(password, user_password)

				if hashed_pw == user.password:
					request.session['user_id'] = user.id
					# request.session['first_name'] = first_name
					
					return redirect('/travels')

			errors.append('Invalid account information.')
		
		for error in errors:
			messages.error(request, error)

		return redirect('/')

		print request.session['user_id']

		print errors

def delete(request, id):
	trip = Trip.objects.get(id=id)
	trip.delete()

	return redirect('/travels')

def logout(request):
	if 'user_id' in request.session:
		request.session.pop('user_id')

	return redirect('/')