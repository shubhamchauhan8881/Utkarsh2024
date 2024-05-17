from django.contrib import admin
from . import models
from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import HttpResponse
from  . import models
from UtkarshWebsite import models as WebsiteModel
import csv
import os
from django.contrib.auth.models import User


@admin.action(description="Export")
def ExportParticipations(modeladmin, request, queryset):
    headers = ["UK id","Name","Event","Category","Gender","Mobile No","Email","College Name","Course","City","CA Refferal","Ambassador","Ambassador id"]
    with open(settings.BASE_DIR / 'UtkarshWebsite/static/temp.csv', "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for partcpns in queryset:
            write_array = [
                partcpns.user.user.username,
                partcpns.user.user.first_name,
                partcpns.event.name,
                partcpns.event.parent_sub_event.parent_event.name,
                partcpns.user.gender,
                partcpns.user.phone,
                partcpns.user.user.email,
                partcpns.user.college_name,
                partcpns.user.course,
                partcpns.user.city,
                partcpns.user.ca_refferal_code,
                "Yes" if partcpns.user.is_ambassador else "No",
                partcpns.user.ambassador_id,
            ]
            # print(write_array)
            writer.writerow(write_array)
    with open(settings.BASE_DIR / f'UtkarshWebsite/static/temp.csv', "r") as f:
        resp = HttpResponse(f.read(),  headers={
            "Content-Type": "application/x-csv",
            "Content-Disposition": 'attachment; filename="Participations.csv" ',
        },)
        return resp
    
class ParticipationsAdmin(admin.ModelAdmin):
    list_display = ["user","date","Name","gender","Phone","college","event","Category_1","Category_2"]
    list_filter = ["event__parent_sub_event__parent_event","date"]
    search_fields = ('Name',)
    actions = (ExportParticipations,)
    
    def Name(self, obj):return obj.user.user.first_name
    def gender(self, obj):return obj.user.gender
    def Phone(self, obj):return obj.user.phone
    def college(self, obj):return obj.user.college_name
    def Category_1(self, obj):return obj.event.parent_sub_event.parent_event
    def Category_2(self, obj):return obj.event.parent_sub_event



@admin.action(description="Export Team Registrations")
def ExportTeamParticipations(modeladmin, request, queryset):
    headers = ["Team Leader UK id", "Leader name","Team Members","Event","Category","Gender","Mobile No","Email","College Name","Course","City","CA Refferal","Ambassador","Ambassador id"]
    with open(settings.BASE_DIR / 'UtkarshWebsite/static/temp2.csv', "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for partcpns in queryset:
            userExtras = WebsiteModel.UserExtras.objects.get(user__username=partcpns.team_leader_uk_id)
            teamMembers = partcpns.team_members.all()
            write_array = [
                userExtras.user.username,
                userExtras.user.first_name,
                ", ".join([x.user.first_name +'('+ x.user.username+')' for x in teamMembers]),
                partcpns.event_registered.name,
                partcpns.event_registered.parent_sub_event.parent_event.name,
                userExtras.gender,
                userExtras.phone,
                userExtras.user.email,
                userExtras.college_name,
                userExtras.course,
                userExtras.city,
                userExtras.ca_refferal_code,
                "Yes" if userExtras.is_ambassador else "No",
                userExtras.ambassador_id,
            ]
            # print(write_array)
            writer.writerow(write_array)
    with open(settings.BASE_DIR / f'UtkarshWebsite/static/temp2.csv', "r") as f:
        resp = HttpResponse(f.read(),  headers={
            "Content-Type": "application/x-csv",
            "Content-Disposition": 'attachment; filename="Participations.csv" ',
        },)
        return resp
    
class TeamParticipationsAdmin(admin.ModelAdmin):
    list_display = ("team_leader_uk_id","team_name","Team_Leader_Name","event_registered", "Team","Category")
    list_filter = ("event_registered__parent_sub_event__parent_event",)
    search_fields = ("team_leader_uk_id",)
    actions = (ExportTeamParticipations, )

    def Category(self, obj):
        return obj.event_registered.parent_sub_event.parent_event.name
    def Team_Leader_Name(self, obj):return User.objects.get(username=obj.team_leader_uk_id).first_name
    def Team(self, obj):
        m = obj.team_members.all()
        return ",".join([x.user.first_name for x in m])



admin.site.register(models.Throwback)
admin.site.register(models.TeamMember)
admin.site.register(models.UtkarshEvents)
admin.site.register(models.SubEvents)
admin.site.register(models.SubSubEvents)
admin.site.register(models.TeamEventRegistrations,TeamParticipationsAdmin)
admin.site.register(models.Accomodation)
admin.site.register(models.Participations, ParticipationsAdmin)