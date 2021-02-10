from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from taggit.managers import TaggableManager
import django
# Create your models here.
class MobileOtp(models.Model):
    mobile_number=models.CharField(max_length=13,blank=False)
    OTP=models.CharField(max_length=4)
    Time=models.DateTimeField()
    def __str__(self):
        return self.mobile_number
class UserProfileInfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="User_user")
    #phone_number=models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    name=models.CharField(max_length=50,default="not avaliable")
    male="Male"
    female="Female"
    others="Others"
    gender_choices=((male,'Male'),(female,'Female'),(others,"Others"))
    Gender=models.CharField(choices=gender_choices,max_length=20)
    date_of_birth = models.DateField()
    #Address=models.CharField(max_length=200)
    uneducated="uneducated"
    fifth="5th Class"
    eight="8th Class"
    Tenth="10th Class"
    Tweleth="12th Class"
    grad="Graduation"
    post="Post Graduation"
    Doctorate="Doctorate"
    edu_choices=((uneducated,"uneducated"),(fifth,"5th Class"),(eight,"8th Class"),(Tenth,'10th Class'),(Tweleth,'12th Class'),(grad,'Graduation'),(post,'Post Graduation'),(Doctorate,'Doctorate'))
    Highest_Education=models.CharField(choices=edu_choices,max_length=20)
    India="India"
    country_choices=((India,"India"),(others,"Others"))
    Country=models.CharField(max_length=20)
    State=models.CharField(max_length=50)
    District=models.CharField(max_length=100)
    constituency_choice=( ( 'PUROLA' , 'Purola'),( 'YAMUNOTRI' , 'Yamunotri'),( 'GANGOTRI' , 'Gangotri'),( 'BADRINATH' , 'Badrinath'),( 'THARALI' , 'Tharali'),( 'KARANPRAYAG' , 'Karanprayag'),( 'KEDARNATH' , 'Kedarnath'),( 'RUDRAPRAYAG' , 'Rudraprayag'),( 'GHANSALI' , 'Ghansali'),( 'DEOPRAYAG' , 'Deoprayag'),( 'NARENDRANAGAR' , 'Narendranagar'),( 'PRATAP' , 'Pratap'),( 'TEHRI' , 'Tehri'),( 'DHANOLTI' , 'Dhanolti'),( 'CHAKRATA' , 'Chakrata'),( 'VIKASNAGAR' , 'Vikasnagar'),( 'SAHASPUR' , 'Sahaspur'),( 'DHARAMPUR' , 'Dharampur'),( 'RAIPUR' , 'Raipur'),( 'RAJPUR' , 'Rajpur'),( 'DEHRADUN' , 'Dehradun'),( 'MUSSOORIE' , 'Mussoorie'),( 'DOIWALA' , 'Doiwala'),( 'RISHIKESH' , 'Rishikesh'),( 'HARIDWAR' , 'Haridwar'),( 'B.H.E.L' , 'B.H.E.L'),( 'JWALAPUR' , 'Jwalapur'),( 'BHAGWANPUR' , 'Bhagwanpur'),( 'JHABRERA' , 'Jhabrera'),( 'PIRANKALIYAR' , 'Pirankaliyar'),( 'ROORKEE' , 'Roorkee'),( 'KHANPUR' , 'Khanpur'),( 'MANGLORE' , 'Manglore'),( 'LAKSAR' , 'Laksar'),( 'HARIDWAR' , 'Haridwar'),( 'YAMKESHWAR' , 'Yamkeshwar'),( 'PAURI' , 'Pauri'),( 'SRINAGAR' , 'Srinagar'),( 'CHAUBATTAKHAL' , 'Chaubattakhal'),( 'LANSDOWNE' , 'Lansdowne'),( 'KOTDWAR' , 'Kotdwar'),( 'DHARCHULA' , 'Dharchula'),( 'DIDIHAT' , 'Didihat'),( 'PITHORAGARH' , 'Pithoragarh'),( 'GANGOLIHAT' , 'Gangolihat'),( 'KAPKOTE' , 'Kapkote'),( 'BAGESHWAR' , 'Bageshwar'),( 'DWARAHAT' , 'Dwarahat'),( 'SALT' , 'Salt'),( 'RANIKHET' , 'Ranikhet'),( 'SOMESHWAR' , 'Someshwar'),( 'ALMORA' , 'Almora'),( 'JAGESHWAR' , 'Jageshwar'),( 'LOHAGHAT' , 'Lohaghat'),( 'CHAMPAWAT' , 'Champawat'),( 'LALKUWA' , 'LalKuwa'),( 'BHIMTAAL' , 'Bhimtaal'),( 'NAINITAL' , 'Nainital'),( 'HALDWANI' , 'Haldwani'),( 'KALABHUNGI' , 'Kalabhungi'),( 'RAMNAGAR' , 'Ramnagar'),( 'JASPUR' , 'Jaspur'),( 'KASHIPUR' , 'Kashipur'),( 'BAJPUR' , 'Bajpur'),( 'GADARPUR' , 'Gadarpur'),( 'RUDRAPUR' , 'Rudrapur'),( 'KICHHA' , 'Kichha'),( 'SITARGANJ' , 'Sitarganj'),( 'NANAK' , 'Nanak'),( 'KHATIMA' , 'Khatima'))
    constituency=models.CharField(choices=constituency_choice,max_length=30)
    follower=models.CharField(max_length=13)
    Number_of_follower=models.IntegerField(default=0)
    def __str__(self):
        return self.user.username
class follower(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
class web_pages(models.Model):
    page_id=models.CharField(max_length=10,blank=False)
    page_name=models.CharField(max_length=30,blank=False,unique=True)
    page_text=models.CharField(max_length=8000,blank=False)
    def __str__(self):
        return self.page_name
