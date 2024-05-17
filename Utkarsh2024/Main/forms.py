from django import forms
import re
from django.core.exceptions import ValidationError
from UtkarshWebsite import models as OldModel
from django.contrib.auth.models import User



class TeamRegForm(forms.Form):
    ukid = forms.CharField(label="Utarsh id: ", required=True)
    team_name = forms.CharField(label="Team Name")
    
    def clean_ukid(self):
        data = self.cleaned_data["ukid"].upper().split(",")

        for i in range(len(data)):
            if data[i] == '' or data[i] == ' ':
                data.pop(i)
            else:
                data[i] = data[i].strip()

        for Id in data:
            # verify utkarsh id: 
            if not User.objects.filter(username=Id).exists():
                raise ValidationError(f"{Id} is invalid Utkarsh id")
        return ",".join(data)

def verifyEmail(email):
    if(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email)):
        return True
    else:
        return False

class LoginForm(forms.Form):
    username = forms.CharField(required=True,label="Email Id/Utkarsh Id")
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    
    def clean_username(self):
        data = self.cleaned_data["username"]
        if verifyEmail(data):
            ukid = User.objects.filter(email=data)
            if ukid.exists():
                return ukid[0].username
            else:
                raise ValidationError("Invalid username or password")
        else:
            return data


class PasswordResetForm(forms.Form):
    email = forms.CharField(label="Email", required=True, strip=True)
    phone = forms.CharField(label="Mobile no", required=True, strip=True)
    password = forms.CharField(label="New password", widget=forms.PasswordInput, required=True)

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 6:
            raise ValidationError("Password must contain at least 6 characters.")
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data["email"]
        phone = cleaned_data["phone"]

        try:
            user = User.objects.get(email=email)
            userExtras = OldModel.UserExtras.objects.get(phone=phone, user = user)
            cleaned_data["user_id"] = user.id
            return cleaned_data
        except:
            raise ValidationError({"password":"We could not find accounts related with provided details"})

        # if 
        #     return cleaned_data
        # else:
        #     raise ValidationError("We could not find accounts related with provided details")


GENDER_CHOICES = [
    ("Select","Select"),
    ("Male","Male"),
    ("Female","Female"),
]
class RegisterForm(forms.Form):

    full_name = forms.CharField(label="Full name", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(required=True, widget= forms.PasswordInput())
    college_name = forms.CharField(label="College Name", required=True, widget=forms.TextInput(attrs={"list":"college_name_suggestions"}))
    city = forms.CharField(label="City", required=True)
    mobile = forms.CharField(label="Phone", required=True)
    gender = forms.ChoiceField(choices = GENDER_CHOICES) 
    course = forms.CharField(label="Course", required=True)
    ca_refferal = forms.CharField(label="CA Refferal", required=False)

    def clean_gender(self):
        data = self.cleaned_data["gender"]
        if data == "Select":
            raise ValidationError("Choose your gender.")
        else:
            return data

        
    def clean_password(self):
        password = self.cleaned_data["password"]

        if len(password) < 6:
            raise ValidationError("Password must contain at least 6 characters.")

        return password

        # if password != re_password:
        #     raise ValidationError("Password and retype password not matched")
 
    def clean_ca_refferal(self):
        ca = self.cleaned_data["ca_refferal"]
        if ca:
            # chec if ca code is correct
            if not OldModel.UserExtras.objects.filter(ambassador_id= ca).exists():
                raise ValidationError("Invalid Ambassador id.")
        return ca
            
    def clean_email(self):
        if not verifyEmail(self.cleaned_data["email"]):
            raise ValidationError("Invalid e-mail!")
        #check if email 
        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise ValidationError("This e-mail is already registered!")
        return self.cleaned_data["email"]


    def clean_mobile(self):
        data = self.cleaned_data["mobile"]
        if not data.isdigit():
            raise ValidationError("Invalid mobile no.")

        if data[0] in [str(i) for i in range(0,6)]:
            raise ValidationError(f"Mobile no can not start with {data[0]}")

        if len(data) != 10:
            raise ValidationError("Invalid mobile no!")
        return data
