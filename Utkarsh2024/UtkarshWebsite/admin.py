from django.contrib import admin
from . import models
import random
from django.http import HttpResponse
from django.conf import settings
import csv
# Regisimter your mode
admin.site.site_header = 'UTKARSH\'24 Administration'

# to export reg users...
@admin.action(description="Export Registered Users")
def export(modeladmin, request, queryset):
    headers = ["UK id", "Name","Gender","Mobile No","Email","College Name","Course","City","CA Refferal","Ambassador","Ambassador id","Accomodation Required"]
    with open(settings.BASE_DIR / 'UtkarshWebsite/static/temp.csv', "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for reg_user in queryset.order_by('user__first_name'):
            write_array = [
                reg_user.user.username,
                reg_user.user.first_name,
                reg_user.gender,
                reg_user.phone,
                reg_user.user.email,
                reg_user.college_name,
                reg_user.course,
                reg_user.city,
                reg_user.ca_refferal_code,
                "Yes" if reg_user.is_ambassador else "No",
                reg_user.ambassador_id,
                reg_user.accomodation_required
            ]
            writer.writerow(write_array)

    with open(settings.BASE_DIR / 'UtkarshWebsite/static/temp.csv', "r") as f:
        resp = HttpResponse(f.read(), content_type='text/csv')
        return resp


def GenerateAmbassadorId():
    tries = 0
    while True:
        ab_id = f"UKCA{random.randrange(1000, 999999)}"
        tries += 1
        if tries >= 5:
            ab_id = f"UKCA{random.randrange(100, 9999999)}"
        #check if id alresy exists or not
        d = models.UserExtras.objects.filter(ambassador_id = ab_id)
        if not d:
            return ab_id

@admin.action(  description="Promote as Ambassador")
def PromoteAmbassador(modeladmin, request, queryset):
    ca_id = GenerateAmbassadorId()
    queryset.update( ambassador_id  = ca_id, is_ambassador = True)

@admin.action( description="Demote from Ambassador")
def DemoteAmbassador(modeladmin, request, queryset):
    queryset.update( ambassador_id  = '', is_ambassador = False)



class UserExtrasModelAdmin(admin.ModelAdmin):
    list_display = ["Utkarsh_id","Name","phone","college_name","gender","city","accomodation_required","ca_refferal_code","is_ambassador","ambassador_id"]
    search_fields = ["user__username", "user__first_name"]
    actions = [PromoteAmbassador,DemoteAmbassador, export]
    list_filter = ["college_name", "gender", "accomodation_required", "is_ambassador"]

    def Utkarsh_id(self, obj):
        return obj.user.username
    def Name(self, obj):
        return obj.user.first_name


# @admin.action(description="Export CA data")
# def exportCaData(modeladmin, request, queryset):
#     headers = ["CA id","Name",]

class AmbassadorRefferalsAdmin(admin.ModelAdmin):
    list_display = ["ca_uk_id", "ambassador_id", "user_uk_id"]
    list_filter = ("ca_uk_id","ambassador_id")


admin.site.register(models.UserExtras, UserExtrasModelAdmin)
admin.site.register(models.RegistrationOn)
admin.site.register(models.AmbassadorRefferals, AmbassadorRefferalsAdmin)