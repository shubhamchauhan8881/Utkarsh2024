import random
from . import forms
from . import models
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout




def GenerateUtkarshId():
    tries = 0
    while True:
        uk_id = f"UK24{random.randrange(1000, 999999)}"
        tries += 1
        if tries >= 8:
            uk_id = f"UK24{random.randrange(100, 9999999)}"
        #check if id alresy exists or not
        d = User.objects.filter(username= uk_id).exists()
        if not d:
            return uk_id


@csrf_exempt
def checkemail(request):
    m = ''
    s = RegisteredUsers.get_by_email(request.POST.get('email'))
    if s:m = "User with email already exists."
    else: m = "GoodToGo"
    return JsonResponse({"message":m})

def get_content_type(k):
    k = k.lower().split('.')[1]
    if k=="jpg" or k== "jpeg" or k== "png":
        return  (f"image/{k}")
    elif k == "pdf":
        return ("application/pdf")
    elif k == 'mp4':
        return ("video/mp4")
    elif k == 'gif':
        return ("image/gif")


def HomePage(request, caid = None):
    if caid == None:
        regForm = forms.RegisterForm()
    else:
        regForm = forms.RegisterForm(data={"ca_refferal": caid})
    
    context = {"form":regForm}
    if caid != None:
        context["Formerrors"] = True

    return render(request, "base.html", context=context)


def RegisterUser(request):
    
    REG_ON  =  models.RegistrationOn.objects.all()[0].taking_registration
    if not REG_ON:
        return HttpResponse("<h1>Registration Closed</h1>")
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            email = form.cleaned_data["email"]
            name = form.cleaned_data["full_name"]
            password = form.cleaned_data["password"]
            college_name = form.cleaned_data["college_name"]
            city = form.cleaned_data["city"]
            mobile = form.cleaned_data["mobile"]
            gender = form.cleaned_data["gender"]
            course = form.cleaned_data["course"]
            ca_refferal = form.cleaned_data["ca_refferal"]

            # if ca refferal given


            user = User.objects.create(
                username = GenerateUtkarshId(),
                first_name = name, 
                email = email
            )
            user.set_password = password
            user.save()

            if ca_refferal:
                ca = models.AmbassadorRefferals(
                    ca_uk_id = models.UserExtras.objects.filter(ambassador_id= ca_refferal)[0].user.username,
                    ambassador_id = ca_refferal,
                    user_uk_id = user.username
                )
                ca.save()

            userExtras = models.UserExtras.objects.create(
                user = user,
                phone = mobile,
                college_name =college_name ,
                course =course,
                gender =gender,
                city = city,
                ca_refferal_code  = ca_refferal
            )

            userExtras.save()
            return render(request, "base.html", {"RegSuccess":True, "ukid":user.username})
        else:
            return render(request, "base.html", {"form":form, "Formerrors":True})



def signout(request):
    logout(request)
    return redirect("homepage")
