from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from . import models
import random
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from UtkarshWebsite import models as UtkarshWebsiteModel
from django.contrib.auth.decorators import login_required

# Create your views here.
def HomePage(request):
    throwback = models.Throwback.objects.all()
    events = models.UtkarshEvents.all_events()
    team_members = models.TeamMember.objects.all()
    return render(request, 'main/homepage.html', {"throwback":throwback,"events":events,"team_members":team_members})

@login_required(redirect_field_name="mainloginpage")
def UserProfile(request):
    userExtras = UtkarshWebsiteModel.UserExtras.objects.get(user=request.user)
    t = None

    # payment summary
    payments = 0
    summary = {}
    p = ["sports","informal"]

    for i in models.Participations.objects.filter(user = userExtras):
        if i.event.parent_sub_event.parent_event.name.lower() in p:
            summary[i.event.name] = i.event.registration_amount
            payments += i.event.registration_amount
    # for team reg
    for j in models.TeamEventRegistrations.objects.filter(team_leader_uk_id = userExtras.user.username):
        c =  j.event_registered.parent_sub_event.parent_event.name
        if c.lower() in p:
            summary[j.event_registered.name] = j.event_registered.registration_amount
            payments += j.event_registered.registration_amount
    
    if userExtras.accomodation_required:
        summary["Accomodation"] = 500
        payments += 500
    
    summary["Total"] = payments
    
    if userExtras.is_ambassador:
        ambassador_refferals = UtkarshWebsiteModel.AmbassadorRefferals.objects.filter(ca_uk_id=userExtras.user.username)
        t = []
        for i in ambassador_refferals:
            ukid = i.user_uk_id
            user = UtkarshWebsiteModel.UserExtras.objects.get(user__username = ukid)
            t.append(user)

    # check solo participations
    solo = models.Participations.objects.filter(user = UtkarshWebsiteModel.UserExtras.objects.get(user = request.user))
    #team participations
    #  [ Event, (members...) ]
    team_p = [x for x in models.TeamEventRegistrations.objects.filter(team_leader_uk_id= request.user.username) ]

    return render(request, "main/user_profile.html", {"userExtras":userExtras, "ambassador_refferals":t,"teamReg":team_p ,"solo":solo, "summary":summary})


def LoginPage(request):
    if request.user.is_authenticated:return redirect("mainhomepage")
    if request.method == 'GET':
        loginform = forms.LoginForm()
        return render(request, 'main/login_page.html', {'loginform':loginform})
    else:
        loginform = forms.LoginForm(request.POST)
        if loginform.is_valid():
            user = authenticate(request, username=loginform.cleaned_data["username"], password=loginform.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect('mainhomepage')
            else:
                loginform.add_error("password", "Invalid username or password")
                return render(request, 'main/login_page.html', {'loginform':loginform})
        else:return render(request, 'main/login_page.html', {'loginform':loginform})


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

def RegisterPage(request):
    return render(request, 'main/reg_closed.html')
    if request.user.is_authenticated:return redirect("mainhomepage")
    if request.method == 'GET':
        register_form = forms.RegisterForm()
        college_name_list= [c.college_name.title() for c in UtkarshWebsiteModel.UserExtras.objects.all()]
        college_name_suggestions = []
        
        for i in college_name_list:
            if  i not in college_name_suggestions:
                college_name_suggestions.append(i)

        return render(request, "main/register_page.html", {'registerform':register_form,"college_name_suggestions":college_name_suggestions, "RegSuccess":False})
    else:
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            name = form.cleaned_data["full_name"]
            password = form.cleaned_data["password"]
            college_name = form.cleaned_data["college_name"]
            city = form.cleaned_data["city"]
            mobile = form.cleaned_data["mobile"]
            gender = form.cleaned_data["gender"]
            course = form.cleaned_data["course"]
            ca_refferal = form.cleaned_data["ca_refferal"]

            user = User.objects.create(
                username = GenerateUtkarshId(),
                first_name = name, 
                email = email
            )
            user.set_password(password)
            user.save()


            if ca_refferal:
                ca = UtkarshWebsiteModel.AmbassadorRefferals(
                    ca_uk_id = UtkarshWebsiteModel.UserExtras.objects.filter(ambassador_id= ca_refferal)[0].user.username,
                    ambassador_id = ca_refferal,
                    user_uk_id = user.username
                )
                ca.save()

            userExtras = UtkarshWebsiteModel.UserExtras.objects.create(
                user = user,
                phone = mobile,
                college_name =college_name ,
                course =course,
                gender =gender,
                city = city,
                ca_refferal_code  = ca_refferal
            )

            userExtras.save()
            login(request, user)
            return render(request,  "main/register_page.html",  {"RegSuccess":True, "ukid":user.username})
        else:
            return render(request, "main/register_page.html", {'registerform':form, "RegSuccess":False}) 


def signout(request):
    logout(request)
    return redirect("mainhomepage")

def Enroll(request, eventid):
    if not request.user.is_authenticated:return redirect("mainhomepage")
    event = models.SubSubEvents.objects.get(id=int(eventid))
    user = UtkarshWebsiteModel.UserExtras.objects.get(user=request.user)

    if not models.Participations.objects.filter(user__user = request.user, event__id = int(eventid) ).exists():
        p = models.Participations.objects.create(
            user = user, 
            event = event
        )
        p.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required( redirect_field_name="mainloginpage")
def UnEnroll(request, eventid):
    try:
        i = models.Participations.objects.filter(id=int(eventid))
        if i.exists():i.delete()
    except:pass
    finally:return redirect(request.META.get('HTTP_REFERER'))

@login_required( redirect_field_name="mainloginpage")
def TeamUnEnroll(request, eventid):
    try:
        i = models.TeamEventRegistrations.objects.filter(id=int(eventid))
        if i.exists():i.delete()
    except Exception as e:
        print(e)
    finally:return redirect(request.META.get('HTTP_REFERER'))

def AccomodationManage(request):
    opt = request.POST.get("accommodation")
    userExtras = UtkarshWebsiteModel.UserExtras.objects.get(user=request.user)
    userExtras.accomodation_required = True if opt == "yes" else False
    userExtras.save()
    return redirect(request.META.get('HTTP_REFERER'))
    

def TeamReg(request, eventid):
    if not request.user.is_authenticated:return redirect("mainhomepage")
    event = models.SubSubEvents.objects.get(id=int(eventid))
    if request.method == "GET":
        form = forms.TeamRegForm()
        return render(request, "main/team_reg.html", {"event":event, "form":form})
    else:
        f = forms.TeamRegForm(request.POST)
        if f.is_valid():
            tm = []
            for Id in f.cleaned_data["ukid"].split(","):
                tm.append(UtkarshWebsiteModel.UserExtras.objects.get(user__username=Id))

            tg = models.TeamEventRegistrations.objects.create(
                team_name=f.cleaned_data["team_name"],
                team_leader_uk_id = request.user.username,
                event_registered = event,
            )
            tg.team_members.add(*tm)
            return render(request, "main/team_reg.html", {"TeamRegSuccess":True,"event":event,"team_members":tm})

        else:
            return render(request, "main/team_reg.html", {"event":event, "form":f})



def EventsPage(request):
    user_enrolled = ''
    if request.user.is_authenticated:
        user_enrolled = [up.event.id for up in models.Participations.objects.filter(user__user = request.user)]

        tr= models.TeamEventRegistrations.objects.filter(team_leader_uk_id = request.user.username)
        for i in tr:
            user_enrolled.append(i.event_registered.id)

        # team_regs = [tr.event.id for tr in models.Participations.objects.filter(user__user = request.user)]

    typ = request.GET.get("q")
    if typ is None or typ == 'all':
        filtered = models.SubSubEvents.objects.all()
    elif typ == "solo":
        filtered = models.SubSubEvents.objects.filter(is_team_event=False)
    elif typ == "team":
        filtered = models.SubSubEvents.objects.filter(is_team_event=True)
    elif typ.isdigit():
        filtered = models.SubSubEvents.get_by_event(int(typ))
            
    events = models.UtkarshEvents.all_events()

    return render(request, "main/events_page.html", {"events":events, "filtered":filtered, "user_enrolled":user_enrolled})


def CaPortal(request):
    return render(request, "main/ca.html")




def ResetPassword(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            data = {"email":request.user.email,"phone":UtkarshWebsiteModel.UserExtras.objects.get(user=request.user).phone}
            f = forms.PasswordResetForm(data=data)
        else:f = forms.PasswordResetForm()
        return render(request, "main/pass-reset-form.html",{"form":f})
    else:
        f = forms.PasswordResetForm(request.POST)
        if f.is_valid():
            userid = int(f.cleaned_data["user_id"])
            password = f.cleaned_data["password"]
            u = User.objects.get(id=userid)
            u.set_password(password)
            u.save()
            return render(request, "main/pass-reset-form.html",{"passResetSuccess":True}) 
        else:
            return render(request, "main/pass-reset-form.html",{"form":f}) 