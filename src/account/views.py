from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from blog.models import BlogPost
# Create your views here.
def registration_view(request):
	context = {}
	
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			std_id = form.cleaned_data.get("std_id")
			raw_password = form.cleaned_data.get("password1")
			account = authenticate(std_id=std_id, password=raw_password)
			login(request, account)
			return redirect('home')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form

	return render(request, "account/register.html", context)

def expired_view(request):
	context = {}
	try:
		del request.session['user']
	except KeyError:
		context['message'] = "Session has expired"
	return render(request, "account/logout.html", context)
	
def logout_view(request):
	logout(request)
	return render(request, "account/logout.html", {})

def login_view(request):
	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect("home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			std_id = request.POST["std_id"]
			password = request.POST["password"]
			user = authenticate(std_id=std_id, password=password)

			if user:
				login(request, user)
				return redirect("home")
	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form
	return render(request, "account/login.html", context)

def account_view(request):
	if not request.user.is_authenticated:
		return redirect("login")

	context = {}

	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
						"upmail": request.POST['upmail'],
						"std_id": request.POST['std_id'],
						"username": request.POST['username'],
						"first_name": request.POST['first_name'],
						"last_name" : request.POST['last_name'],
			}
			form.save()
			context['success_message']="Successfully updated"
	else:
		form = AccountUpdateForm(
				initial = {
						"upmail": request.user.upmail,
						"std_id": request.user.std_id,
						"username": request.user.username,
						"first_name": request.user.first_name,
						"last_name" : request.user.last_name,
				}
			)

	context['account_form'] = form

	blog_posts = BlogPost.objects.filter(author=request.user)
	context['blog_posts'] = blog_posts
	return render(request, 'account/account.html', context)

def must_authenticate_view(request):
	return render(request, 'account/must_authenticate.html', {})