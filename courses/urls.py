from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list, name='courses'),
    path('courses/<int:course_id>/add_video/', views.add_video, name='add_video'),
    path('add-course/', views.add_course, name='add_course'),
    path('courses/<int:course_id>/enroll_student/', views.enroll_student, name='enroll_student'),
    path('courses/<int:course_id>/self_enroll/', views.self_enroll, name='self_enroll'),
    path('approve-enrollment/<int:request_id>/', views.approve_enrollment, name='approve_enrollment'),
]