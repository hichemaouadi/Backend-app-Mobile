from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_employee , name="login"),
    path('logout/',views.logout_employee, name="logout")
]