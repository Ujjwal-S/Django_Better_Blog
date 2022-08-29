from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

genders = (
	('m', 'Male'),
	('f', 'Female')
)


class CustomAccountManager(BaseUserManager):
	def create_superuser(self, email, username, password, **other_fields):
		other_fields.setdefault('is_staff', True)
		other_fields.setdefault('is_superuser', True)
		other_fields.setdefault('is_active', True)

		if other_fields.get('is_staff') is not True:
			raise ValueError(
				'Superuser must be assigned to is_staff=True.')
		if other_fields.get('is_superuser') is not True:
			raise ValueError(
				'Superuser must be assigned to is_superuser=True.')

		return self.create_user(email, username, password, **other_fields)

	def create_user(self, email, username, password, **other_fields):

		if not email:
			raise ValueError('You must provide an email address')

		email = self.normalize_email(email)
		user = self.model(email=email, username=username,
						  **other_fields)
		user.set_password(password)
		user.save()
		return user



class User(AbstractBaseUser, PermissionsMixin):

	email = models.EmailField('email address', unique=True)
	username = models.CharField(max_length=150, unique=True)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	objects = CustomAccountManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	def __str__(self):
		return self.username


countries = (
	('India', 'India'),
	('United States', 'United States'),
	('Spain', 'Spain'),
	('Germany', 'Germany'),
	('France', 'France')
)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	birthday = models.DateField(blank=True, null=True)
	gender = models.CharField(choices=genders, blank=True, max_length=10, null=True)
	phone = models.CharField(max_length=20, blank=True, null=True)
	img = models.ImageField(upload_to='users', default='users/default-user.jpg')

	def __str__(self):
		return self.user.username

class UserSession(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	device = models.CharField(max_length=200)
	device_type = models.CharField(max_length=20)
	browser = models.CharField(max_length=200)
	login_time = models.DateTimeField(auto_now_add=True)
	sess_key = models.CharField(max_length=200)


	def __str__(self):
		return f'{self.user.username} - {self.device}'
