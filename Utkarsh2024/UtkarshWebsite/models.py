from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class RegistrationOn(models.Model):
    taking_registration = models.BooleanField(default=False)

    def __str__(self):
        return str(self.taking_registration)



class UserExtras(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    phone = models.CharField(max_length=12, null=True, blank=True)
    college_name = models.CharField(max_length=250  , null=True, blank=True)
    course = models.CharField(max_length=100 , null=True, blank=True)
    gender = models.CharField(max_length=10 , null=True, blank=True)
    city = models.CharField(max_length=300, null=True, blank=True)
    ca_refferal_code  = models.CharField(max_length=50, null=True, blank=True)

    # enrolled events....(individual)
    # enrolled_events = models.ManyToManyField(SubSubEvents, blank=True)
    #ca refferal...
    is_ambassador = models.BooleanField(default=False)
    ambassador_id = models.CharField(max_length=20, null=True, blank=True)

    accomodation_required = models.BooleanField(default=False)

    

    reg_fee = models.IntegerField(default=0)
    extra_charges = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class AmbassadorRefferals(models.Model):
    # the person who used his refferal ( ambassador )
    ca_uk_id = models.CharField(max_length=200, null=True, blank=True)  
    ambassador_id = models.CharField(max_length=200, null=True, blank=True)
    # user is who is using ca id refferal
    user_uk_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return User.objects.get(username=self.ca_uk_id).first_name

