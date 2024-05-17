from django import forms
import re
from django.core.exceptions import ValidationError
from . import models
from django.contrib.auth.models import User


GENDER_CHOICES = [
    ("Select","Select"),
    ("Male","Male"),
    ("Female","Female"),
]
class RegisterForm(forms.Form):

    full_name = forms.CharField(label="Full name", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(required=True, widget= forms.PasswordInput())
    college_name = forms.CharField(label="College Name", required=True)
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
            if not models.UserExtras.objects.filter(ambassador_id= ca).exists():
                raise ValidationError("Invalid Ambassador id.")
        return ca
            
    def clean_email(self):
        if not self.verifyEmail(self.cleaned_data["email"]):
            raise ValidationError("Invalid e-mail!")

        #check if email 
        if User.objects.filter(username=self.cleaned_data["email"]).exists():
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




    def verifyEmail(self, email):
        if(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email)):
            return True
        else:
            return False
