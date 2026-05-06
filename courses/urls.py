from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list, name='courses'),
    path('courses/<int:course_id>/add_video/', views.add_video, name='add_video'),
]