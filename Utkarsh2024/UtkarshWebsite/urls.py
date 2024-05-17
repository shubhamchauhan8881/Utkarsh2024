
from django.urls import path,include
from . import views
urlpatterns = [
    path("", views.HomePage, name="homepage"),
    path("user/register/", views.RegisterUser),
    path("user/logout/", views.signout),
    path("refferals/ambassador/<str:caid>", views.HomePage),
]


