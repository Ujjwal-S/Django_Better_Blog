from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('email', 'password1', 'password2')

	def save(self, commit=True):
		user = super(UserRegisterForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		username = user.email.split('@')[0]
		if User.objects.filter(username=username).exists():
			raise ValidationError("Please check your email address.")
		user.username = username
		user.is_active = False

		if commit:
			user.save()
		return user


class UpdateProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = '__all__'
		exclude = ('user',)