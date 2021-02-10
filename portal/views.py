from django.shortcuts import render,get_object_or_404,get_list_or_404
from django import forms
from django.views.decorators.cache import cache_control
from portal.forms import UserForm,UserProfileInfoForm,MobileOtpForm,OtpVerify,DOBVerify
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from portal.models import UserProfileInfo,User,MobileOtp,web_pages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import boto3,random
from django import utils

def welcome(request):
    if(request.user.is_authenticated):
        try:
            UserProfile=UserProfileInfo.objects.get(user=request.user)
        except UserProfileInfo.DoesNotExist:
            UserProfile=None
        if(UserProfile==None):
            error=1
            error_message="Unable to find user please contact Support team of Kranti Vahini IT Cell."
            return render(request,"welcome.html",{"UserProfile":UserProfile,"error":error,"error_message":error_message})
        else:
            follower_count=UserProfileInfo.objects.filter(follower=UserProfile.user).count()
            return render(request,"welcome.html",{"UserProfile":UserProfile,"follower_count":follower_count})
    else:
        if(request.method=="POST"):
            mobileotp_Form=MobileOtpForm(data=request.POST)
            try:
                user=User.objects.get(username=request.POST.get('mobile_number'))
            except User.DoesNotExist:
                user=None
            if(True):
                client = boto3.client(
                    "sns",
                    #your access and security keys
                    region_name="ap-south-1",
                )
                # Send your sms message.
                if(user==None and mobileotp_Form.is_valid()):
                    OTP=str(random.randint(1000,9999))
                    mobileno=request.POST.get('mobile_number')
                    try:
                        otp_form=MobileOtp.objects.get(mobile_number=mobileno)
                    except MobileOtp.DoesNotExist:
                        otp_form=mobileotp_Form.save(commit=False)
                    otp_form.OTP=str(OTP)
                    otp_form.Time=utils.timezone.now()
                    res=client.publish(PhoneNumber=("+91"+str(request.POST.get('mobile_number'))),Message=("Your OTP for Kranti Vahini is - "+OTP+" ."),MessageAttributes={'AWS.SNS.SMS.SenderID':{"DataType":"String",'StringValue':'UKTOTPTXN'},}),
                    print(request.POST.get('mobile_number'),res)
                    otp_form.save()
                    request.session['mobile_number'] = str(request.POST.get('mobile_number'))
                    return HttpResponseRedirect(reverse('OTP_verify'))
                else:
                    if(True):
                        request.session['mobile_number'] = str(request.POST.get('mobile_number'))
                        return HttpResponseRedirect(reverse('DOB_verify'))
        else:
            mobileotp_Form=MobileOtpForm()
            return render(request,'welcome.html',{'mobileotp_Form':mobileotp_Form})
def register_another(request):
    if(request.method=="POST"):
        mobileotp_Form=MobileOtpForm(data=request.POST)
        try:
            user=User.objects.get(username=request.POST.get('mobile_number'))
        except User.DoesNotExist:
            user=None
        if(True):
            # Send your sms message.
            if(user==None and mobileotp_Form.is_valid()):
                client = boto3.client(
                    "sns",
                    #your access and security keys
                    region_name="ap-south-1",
                )
                OTP=str(random.randint(1000,9999))
                mobileno=request.POST.get('mobile_number')
                try:
                    otp_form=MobileOtp.objects.get(mobile_number=mobileno)
                except MobileOtp.DoesNotExist:
                    otp_form=mobileotp_Form.save(commit=False)
                otp_form.OTP=str(OTP)
                otp_form.Time=utils.timezone.now()
                res=client.publish(PhoneNumber=("+91"+str(request.POST.get('mobile_number'))),Message=("Your OTP for Kranti Vahini is - "+OTP+" ."),MessageAttributes={'AWS.SNS.SMS.SenderID':{"DataType":"String",'StringValue':'UKTOTPTXN'},}),
                print(request.POST.get('mobile_number'),res)
                otp_form.save()
                request.session['mobile_number_new_user'] = str(request.POST.get('mobile_number'))
                return HttpResponseRedirect(reverse('OTP_verify'))
            else:
                if(True):
                    #request.session['mobile_number'] = str(request.POST.get('mobile_number'))
                    error=1
                    error_message="User is already present with the Mobile Number you entered "
                    return render(request,'register_another.html',{'mobileotp_Form':mobileotp_Form,'error':error,'error_message':error_message,})

    else:
        mobileotp_Form=MobileOtpForm()
    return render(request,'register_another.html',{'mobileotp_Form':mobileotp_Form})
def DOB_verify(request):
    if(request.method=="POST"):
        DOBform=DOBVerify(data=request.POST)
        if(DOBform.is_valid()):
            mobile_number=request.session['mobile_number']
            user=User.objects.get(username=mobile_number)
            UserProfileInfo_obj=UserProfileInfo.objects.get(user=user)
            print(request.POST.get('DOB'),UserProfileInfo_obj.date_of_birth,request.POST.get('DOB')==UserProfileInfo_obj.date_of_birth)
            if(str(request.POST.get('DOB'))==str(UserProfileInfo_obj.date_of_birth)):
                request.session['validation']=True
                if(user.is_active):
                    login(request,user)
                    user_test=user
                    return HttpResponseRedirect(reverse('welcome'))
                else:
                    return HttpResponse("ACCOUNT IS NOT ACTIVE")
                #return HttpResponseRedirect(reverse('register'))
            else:
                error=1
                error_message="Date of Birth didn't match with the records."
                return render(request,'DOBverify.html',{'DOBForm':DOBform,'error':error,'error_message':error_message})
    else:
        DOBform=DOBVerify()
    return render(request,'DOBverify.html',{'DOBForm':DOBform,})
def OTP_verify(request):
    if(request.method=="POST"):
        OTPform=OtpVerify(data=request.POST)
        if(OTPform.is_valid()):
            if(request.user.is_authenticated):
                mobile_no=request.session['mobile_number_new_user']
            else:
                mobile_no=request.session['mobile_number']
            mobileOtp=MobileOtp.objects.get(mobile_number=mobile_no)
            #UserProfileInfo_obj=UserProfileInfo.objects.get(user=user)
            if(request.POST.get('OTP_Number')==mobileOtp.OTP):
                if(request.user.is_authenticated):
                    request.session['validation_new_user']=True
                else:
                    request.session['validation']=True
                return HttpResponseRedirect(reverse('register'))
            else:
                error=1
                error_message="Incorrect OTP, Please try again..."
                return render(request,'otpverify.html',{'OTPForm':OTPform,'error':error,'error_message':error_message})
    else:
        OTPform=OtpVerify()
    return render(request,'otpverify.html',{'OTPForm':OTPform,})
def show(request,page_req=0):
    page=get_object_or_404(web_pages,page_id=page_req)
    page_name=page.page_name
    page_text=page.page_text
    return render(request,'show.html',{'page_name':page_name,'page_text':page_text})
def register(request):
    registered=0
    if(request.method=="POST"):
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)
        updated_data = request.POST.copy()
        if(request.user.is_authenticated):
            updated_data.update({'username': str(request.session['mobile_number_new_user'])})
        else:
            updated_data.update({'username': str(request.session['mobile_number'])})
        if(request.POST.get('follower')==None):
            print(request.session['follower'])
            updated_data.update({'follower':request.session['follower']})
        user_form=UserForm(data=updated_data)
        profile_form=UserProfileInfoForm(data=updated_data)
        print(request.POST.get('follower'))
        value_of_mobile_number='0000000000'
        try:
            if(request.POST.get('follower')==None):
                user_find=User.objects.get(username=request.session['follower'])
            else:

                #user_find=User.objects.get(username=request.POST.get('follower'))
                #value_of_mobile_number='8979180488'
                request.session['follower']=value_of_mobile_number
                user_find=User.objects.get(username=request.POST.get(value_of_mobile_number))
            #updated_data.update({'follower': user_find})
            #print(profile_form)
        except User.DoesNotExist:
            error=1
            error_message="Follower with this mobile number doesn't exist."
            invalid_follower=1
            mobile_number_val=request.session['mobile_number']
            print(error_message)
            return render(request,'register.html',{'user_form':user_form,'profile_form':profile_form,'mobile_number_val':mobile_number_val,'error':error,'error_message':error_message})
        #user_form.cleaned_data['username'] = str(request.session['mobile_number'])
        if(user_form.is_valid() and profile_form.is_valid()):
            if(request.user.is_authenticated):
                #print("Authenticated User is trying to register")
                new_user=user_form.save(commit=False)
                new_user.username=request.session['mobile_number_new_user']
                #print("Temp details are saved")
                #print(new_user)
                new_user.save()
                profile=profile_form.save(commit=False)
                #user_find=User.objects.get(username=request.POST.get('follower'))
                userprofile_find=UserProfileInfo.objects.get(user=user_find)
                userprofile_find.Number_of_follower+=1
                userprofile_find.save()
                profile.user=new_user
                profile.name=new_user.first_name
                print(profile)
                print(profile_form)
                profile.save()
                return HttpResponseRedirect(reverse('new_user_registered'))
            else:
                user=user_form.save(commit=False)
                user.username=request.session['mobile_number']
                user.save()
                profile=profile_form.save(commit=False)
                user_find=User.objects.get(username=value_of_mobile_number)
                #user_find=User.objects.get(username=request.POST.get('follower'))
                userprofile_find=UserProfileInfo.objects.get(user=user_find)
                userprofile_find.Number_of_follower+=1
                userprofile_find.save()
                profile.user=user
                profile.name=user.first_name
                profile.save()
                if(user.is_active):
                    login(request,user)
                    user_test=user
                    return HttpResponseRedirect(reverse('welcome'))
                else:
                    return HttpResponse("ACCOUNT IS NOT ACTIVE")
        else:
            if(request.session['validation']==True):
                mobile_number_val=request.session['mobile_number']
                return render(request,'register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered,'mobile_number_val':mobile_number_val})
            else:
                return HttpResponseRedirect(reverse('welcome'))
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()
        if(request.user.is_authenticated and request.session['validation_new_user']):
            mobile_number_val=request.session['mobile_number_new_user']
            having_follower=1
            follower_number=request.session['mobile_number']
            request.session['follower']=follower_number
            return render(request,'register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered,'mobile_number_val':mobile_number_val,'having_follower':having_follower,'follower_number':follower_number})
        else:
            if(request.session['validation']):
                mobile_number_val=request.session['mobile_number']
                having_follower=1
                follower_number="0000000000"
                request.session['follower']=follower_number
                return render(request,'register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered,'mobile_number_val':mobile_number_val,'having_follower':having_follower,'follower_number':follower_number})
            else:
                return HttpResponseRedirect(reverse('welcome'))
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('welcome'))
def donate(request):
    return render(request,'donate.html')
@login_required
def new_user_registered(request):
    return render(request,'new_user_registered.html')

# Create your views here.
