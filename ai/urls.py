from django.urls import path

from . import views

urlpatterns = [

    path("chat/", views.chat, name="chat"),

    path("clear/", views.clear_chat, name="clear_chat"),

]