
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from django.contrib import sitemaps
from django.urls import reverse

from Main import models

class EventsSiteMap(sitemaps.Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return models.UtkarshEvents.objects.all()
    
    def location(self,obj):

        return f"/events/?q={obj.id}"


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return ["mainhomepage", "maineventspage", "mainloginpage","ca","mainregisterpage" ]

    def location(self, item):
        return reverse(item)



sitemaps = {
    "static": StaticViewSitemap,
    "EventsSiteMap":EventsSiteMap,
}


urlpatterns = [
    path("sitemap.xml",sitemap,{"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap",),
    path("", views.HomePage, name="mainhomepage"),
    path("ca/", views.CaPortal, name="ca"),
    path("user-profile/", views.UserProfile, name=""),
    path("login/", views.LoginPage, name="mainloginpage"),
    path("logout/", views.signout),
    path("register/", views.RegisterPage, name="mainregisterpage"),
    path("events/", views.EventsPage, name="maineventspage"),
    path("team-registration/<int:eventid>", views.TeamReg),
    path("events/participate/<int:eventid>", views.Enroll, name=""),
    path("events/unenroll/<int:eventid>", views.UnEnroll, name=""),
    path("events/unenroll/team/<int:eventid>", views.TeamUnEnroll, name=""),
    path("manageAccomodation/", views.AccomodationManage, name=""),
    path("reset-password", views.ResetPassword,)

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


