from django import forms
from django.contrib.auth.models import User
from portal.models import UserProfileInfo,MobileOtp,web_pages
import datetime
from django.contrib.admin.widgets import AdminDateWidget
from kranti_vahini import settings
from django.contrib import admin
import csv
from django.http import HttpResponse
#@cache_control(no_cache=True, must_revalidate=True, no_store=True)
class OtpVerify(forms.Form):
    OTP_Number=forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control ','pattern':'[0-9]{4}','placeholder':'Enter Your OTP','title':'OTP should be of 4 Digits only'}))
    #fields=('OTP_Number',)

class DOBVerify(forms.Form):
    DOB=forms.DateField(required=True,widget=forms.TextInput(attrs={'class':'form-control','type':'Date',}),label='Date of Birth')
class UserForm(forms.ModelForm):
    #password=forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        error_css_class = "error"
        help_texts = {
            'username': None,
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','Disabled':'true'}),
            #'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'E-mail ID'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Your Name'}),
            #'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Last Name'}),
        }
        labels={
            'username':'Mobile Number',
            'first_name': 'Name',

        }
        fields=( 'username','first_name')

class MobileOtpForm(forms.ModelForm):
    class Meta():
        model=MobileOtp
        error_css_class = "error"

        #mobile_number=forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control ','pattern':'[0-9]{10}','placeholder':'Enter Mobile Number','title':'Mobile number should be of 10 Digits only'}),error_messages={'required': 'Please let us know what to call you!'})
        #MaxValueValidator=1000000000,MinValueValidator=9999999999,
        #OTP=forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control','pattern':'[0-9]{4}','placeholder':'Enter OTP','title':'OTP should be of 4 Digits only'}),error_messages={'required': 'Please let us know what to call you!'})
        widgets = {
            'mobile_number' : forms.TextInput(attrs={'type':'tel','class': 'form-control', 'pattern':'[0-9]{10}','placeholder':'Enter your Mobile','title':'Mobile number should be of 10 Digits only'}),
            #'OTP': forms.TextInput(attrs={'class': 'form-control', 'pattern':'[0-9]{4}','placeholder':'Enter OTP'}),
            #'follower': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Your High School Name'}),
            #'graduation': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Your Graduation School Name'}),
            #'date_of_birth': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input','data-target': '#datetimepicker1'}),
        }
        fields=('mobile_number',)
class webpage_form(forms.ModelForm):
    page_text=forms.CharField(widget=forms.Textarea)
    class Meta():
        model=web_pages
        fields=('page_id','page_name','page_text')
class webpage_admin(admin.ModelAdmin):
    form=webpage_form
class UserProfileInfo_admin(admin.ModelAdmin):
    list_display = ('user','name','Gender','date_of_birth','Country','State','District','constituency','Highest_Education','follower',)
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(UserProfileInfo)
class UserProfileInfoAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display =  ('user','name','Gender','date_of_birth','Country','State','District','constituency','Highest_Education','follower','Number_of_follower')
    list_filter = ('user','name','Gender','date_of_birth','Country','State','District','constituency','Highest_Education','follower','Number_of_follower')
    actions = ["export_as_csv"]
class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        error_css_class = "error"
        model = UserProfileInfo
        #date_of_birth = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
        #date_of_birth = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y',attrs={'type':'date','class': 'form-control'}), input_formats=settings.DATE_INPUT_FORMATS,)
        #date_of_birth = forms.DateField(widget=AdminDateWidget)
        widgets = {
            'Gender': forms.Select(attrs={'class': 'form-control', 'placeholder':'Gender'}),
            'date_of_birth' : forms.TextInput(attrs={'type':'date','class': 'form-control'}),
            'Country': forms.Select(attrs={'class': 'form-control', 'placeholder':'Country', 'id':'country', 'onchange':'DisableDropdown()'}),
            'State':forms.Select(attrs={'class': 'form-control', 'id':'stateId'}),
            'District':forms.Select(attrs={'class': 'form-control', 'id':'cityId'}),
            'Highest_Education': forms.Select(attrs={'class': 'form-control', 'placeholder':'Your Highest Education'}),
            'constituency': forms.Select(attrs={'class': 'form-control',}),
            'follower': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Follower Mobile number','pattern':'[0-9]{10}','title':'Mobile number of follower should be of 10 Digits only'}),
            #'follower': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Your High School Name'}),
            #'graduation': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Your Graduation School Name'}),
            #'date_of_birth': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input','data-target': '#datetimepicker1'}),
        }
        labels={
            'follower':'Mobile No. of follower',
        }
        fields=('Gender','date_of_birth','Country','State','District','constituency','Highest_Education','follower')
