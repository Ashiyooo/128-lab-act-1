from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class AccountManager(BaseUserManager):
	def create_user(self, upmail, username, first_name, last_name, std_id, password=None):
		if not upmail:
			raise ValueError("Users must have a upmail address")
		if "@up.edu.ph" not in upmail:
			raise ValueError("Users must have a valid upmail address")
		if not username:
			raise ValueError("Users must have a username")
		if not first_name:
			raise ValueError("Users must have a first name")
		if not last_name:
			raise ValueError("Users must have a last name")
		if not std_id:
			raise ValueError("Users must have a student ID")
		
		user = self.model(
				upmail = self.normalize_email(upmail),
				username = username,
				first_name = first_name,
				last_name = last_name,
				std_id = std_id,
			)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, std_id, upmail, first_name, last_name, username, password):
		user = self.create_user(
				upmail = self.normalize_email(upmail),
				username = username,
				first_name = first_name,
				last_name = last_name,
				std_id = std_id,
				password = password,
			)

		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class Account(AbstractBaseUser):
	#required by django
	upmail = models.EmailField(verbose_name="upmail", max_length=60, unique=True)
	username = models.CharField(max_length=30, unique=True)
	date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
	last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	#Things I want
	first_name = models.CharField(verbose_name="first name", max_length=40)
	last_name = models.CharField(verbose_name="last name", max_length=40)
	std_id = models.IntegerField(verbose_name="student ID", unique=True)

	USERNAME_FIELD = "std_id"
	REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'upmail']

	objects = AccountManager()

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True