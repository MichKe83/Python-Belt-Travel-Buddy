from __future__ import unicode_literals
from django.db import models
import bcrypt, re, datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def validateRegistration(self, form_data):
		errors = []

		if not EMAIL_REGEX.match(form_data['email']):
			errors.append('An email in valid email format is required.')
		else:
			reg_check = User.objects.filter(email = form_data['email'])
			if reg_check:
				errors.append('The email you are trying to create an account with has already been used.')

		if len(form_data['first_name']) < 2:
			errors.append('First Name is required.')
		if len(form_data['last_name']) <2:
			errors.append('Last Name is required.')
		if len(form_data['email']) == 0:
			errors.append('Email is required.')
		if len(form_data['password']) < 8:
			errors.append('Invalid Password')
		if form_data['password'] != form_data['passwordconf']:
			errors.append('Passwords do not match.')
		
		return errors

	def validateLogin(self, form_data):
		errors = []

		if len(form_data['email']) == 0:
			errors.append('Email is required.')
		if len(form_data['password']) == 0:
			errors.append('Password is required.')	

		return errors

	def createUser(self, form_data):
		password = str(form_data['password'])
		hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

		user = User.objects.create(
			first_name = form_data['first_name'],
			last_name = form_data['last_name'],
			email = form_data['email'],
			password = hashed_pw,
		)

		return user

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.EmailField()
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = UserManager()

class TripManager(models.Manager):
	def validateRegistration(self, form_data):
		errors = []

		date = self.cleaned_data['date']

		if len(form_data['destination']) == 0:
			errors.append('Destination is required.')
		if len(form_data['plan']) == 0:
			errors.append('Plan is required.')
		if len(form_data['start_date']) == 0:
			errors.append('Travel date is required.')
		if len(form_data['end_date']) == 0:
			errors.append('Travel date is required.')
		if form_data['start_date'] < datetime.date.today():
			errors.append('Future date is required.')

		return errors 


class Trip(models.Model):
	user = models.ForeignKey(User, related_name='trips')
	destination = models.CharField(max_length=255)
	plan = models.TextField()
	start_date = models.DateField()
	end_date = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = TripManager()