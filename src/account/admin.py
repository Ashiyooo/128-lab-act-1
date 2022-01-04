from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account
# Register your models here.

class AccountAdmin(UserAdmin):
	list_display = ('upmail', 'username', 'std_id','date_joined', 'last_login', 'is_admin', 'is_staff')
	search_fields = ('upmail', 'username', 'std_id')
	readonly_fields = ('date_joined', 'last_login')

	#required by django
	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(Account, AccountAdmin)