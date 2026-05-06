from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, CourseVideo

# Create your views here.
@login_required
def course_list(request):
    if request.user.role == 'student':
        courses = request.user.enrolled_courses.all()
    elif request.user.role == 'trainer':
        courses = Course.objects.filter(videos__added_by=request.user).distinct()
    else:
        courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def add_video(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.user.role != 'trainer':
        return redirect('home')
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        title = request.POST.get("title")
        youtube_link = request.POST.get("youtube_link")
        CourseVideo.objects.create(
            course=course,
            title=title,
            youtube_link=youtube_link,
            added_by=request.user
        )
        return redirect("courses")
    return render(request, 'courses/add_video.html', {'course': course})