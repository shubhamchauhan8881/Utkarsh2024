from django.db import models
from UtkarshWebsite import models as WebsiteModel

# Create your models here.
class Throwback(models.Model):
    image = models.ImageField(upload_to="uploads/throwback/")


class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'uploads/team/')
    about = models.CharField(max_length=50, blank=True)
    insta_url = models.CharField(blank=True, max_length=500)
    linked_in = models.CharField(blank=True, max_length = 500)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all():
        return TeamMember.objects.all()

class UtkarshEvents(models.Model):
    name = models.CharField(max_length=100)
    mini_description = models.CharField(max_length=600)
    image =  models.ImageField(upload_to = 'uploads/EventsImages/')#home screen poster.....
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def all_events():
        return UtkarshEvents.objects.all()

class SubEvents(models.Model):
    parent_event = models.ForeignKey(UtkarshEvents, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    mini_description = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all():
        return SubEvents.objects.all()
    @staticmethod
    def get_by_id(e):
        return SubEvents.objects.filter(parent_event_id = e)
#main event that will be diplayed as cards.. participation will be donne on the id of this...
class SubSubEvents(models.Model):
    name = models.CharField(max_length=200)
    parent_sub_event = models.ForeignKey(SubEvents, on_delete=models.CASCADE)
    image =  models.ImageField(upload_to = 'uploads/SubEventsImages/')
    mini_description = models.CharField(max_length=1000)
    descp = models.TextField(max_length=6000)
    is_team_event = models.BooleanField(default=False)
    registration_amount = models.IntegerField(default=0)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_by_event(id):
        return SubSubEvents.objects.filter(parent_sub_event__parent_event__id = id)

    @staticmethod
    def get_all():
        return SubSubEvents.objects.all()
    @staticmethod
    def get_by_parent_id(e):
        return SubSubEvents.objects.filter(parent_sub_event_id = e)
    @staticmethod
    def get_by_id(e):
        return SubSubEvents.objects.filter(id=e)

class TeamEventRegistrations(models.Model):
    #it will be the leader if any group registration...
    team_name = models.CharField(max_length=50,default="NA")
    team_leader_uk_id = models.CharField(max_length=50)
    event_registered = models.ForeignKey(SubSubEvents, on_delete=models.CASCADE)

    #has team...
    team_members = models.ManyToManyField(to=WebsiteModel.UserExtras)

    fee = models.IntegerField(default=0)
    extra_charges = models.IntegerField(default=0)

    #paid True, Unpaid False
    payments_status =  models.BooleanField(default=False)

    def __str__(self):
        return self.team_leader_uk_id + "/" + self.event_registered.name
    @staticmethod
    def get_by_uk_id(tlukid):
        return TeamEventRegistrations.objects.filter(team_leader_uk_id=tlukid)


class Participations(models.Model):
    user = models.ForeignKey(WebsiteModel.UserExtras, on_delete=models.CASCADE)
    event = models.ForeignKey(SubSubEvents, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.user.user.username

class Accomodation(models.Model):
    person = models.ForeignKey(WebsiteModel.UserExtras, on_delete=models.CASCADE)
    amount = models.IntegerField(default=500)

    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.person.user.first_name + "/" + self.person.user.username

    @staticmethod
    def get_by_person_id(pid):
        return Accomodation.objects.filter(person_id = pid)