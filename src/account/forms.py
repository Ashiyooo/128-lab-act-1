from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account

class RegistrationForm(UserCreationForm):
	upmail = forms.EmailField(max_length=69, help_text = "Enter your upmail")

	class Meta:
		model = Account
		fields = ("upmail", "username", "first_name", "last_name", "std_id", "password1", "password2")

class AccountAuthenticationForm(forms.ModelForm):
	password = forms.CharField(label="Password", widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ("std_id", "password")

	def clean(self):
		if self.is_valid():
			std_id = self.cleaned_data["std_id"]
			password = self.cleaned_data["password"]
			if not authenticate(std_id=std_id, password=password):
				raise forms.ValidationError("Invalid login")

class AccountUpdateForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ('upmail', 'std_id', 'username')

	def clean_upmail(self):
		if self.is_valid():
			upmail = self.cleaned_data['upmail']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(upmail='upmail')
			except Account.DoesNotExist:
				return upmail 
			raise forms.ValidationError("Upmail '%s' is already in use." % account.upmail)

	def clean_std_id(self):
		if self.is_valid():
			std_id = self.cleaned_data['std_id']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(std_id=std_id)
			except Account.DoesNotExist:
				return std_id 
			raise forms.ValidationError("Student ID '%s' is already in use." % account.std_id)

	def clean_username(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
			except Account.DoesNotExist:
				return username
			raise forms.ValidationError("Username '%s' is already in use." % account.username)

