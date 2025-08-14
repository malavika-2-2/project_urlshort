from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path("<str:code>", views.redirect_short, name="redirect_short"),
]