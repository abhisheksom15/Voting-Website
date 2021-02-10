from django.contrib import admin
from portal.models import UserProfileInfo,MobileOtp,web_pages
from portal.forms import webpage_admin,UserProfileInfo_admin

# Register your models here.

#admin.site.register(UserProfileInfo,UserProfileInfo_admin)
admin.site.register(MobileOtp)
admin.site.register(web_pages,webpage_admin)
