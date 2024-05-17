from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("Main.urls")),
    path("old", include("UtkarshWebsite.urls")),
]
