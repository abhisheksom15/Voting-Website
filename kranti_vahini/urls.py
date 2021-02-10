"""kranti_vahini URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from portal import views
from django.contrib.auth.decorators import login_required
admin.site.site_header = 'Kranti Vahini Staff Login'                    # default: "Django Administration"
admin.site.index_title = 'Welcome to Control Room'                 # default: "Site administration"
admin.site.site_title = 'HTML title from adminsitration'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.welcome,name='welcome'),
    path('donate/',views.donate,name='donate'),
    path('show/<str:page_req>',views.show,name='show'),
    path('welcome/',views.welcome,name='welcome'),
    path('register/',views.register,name='register'),
    path('OTP_verify/',views.OTP_verify,name='OTP_verify'),
    path('DOB_verify/',views.DOB_verify,name='DOB_verify'),
    path('register_another/',views.register_another,name='register_another'),
    path('new_user_registered/',views.new_user_registered,name='new_user_registered'),
    path('user_logout/',views.user_logout,name='user_logout'),
    #path('question_app/',include('question_app.urls')),


]
