from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("word/<entry_id>", views.word, name="word")
]