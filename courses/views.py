from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, CourseVideo, EnrollmentRequest
from users.models import CustomUser

# Create your views here.
@login_required
def course_list(request):

    if request.user.role == "student":

        enrolled_courses = request.user.enrolled_courses.all()

        available_courses = Course.objects.exclude(
            assigned_students=request.user
        )

        return render(
            request,
            "courses/course_list.html",
            {
                "enrolled_courses": enrolled_courses,
                "available_courses": available_courses
            }
        )

    elif request.user.role == "trainer":

        courses = Course.objects.filter(
            videos__added_by=request.user
        ).distinct()

    else:

        courses = Course.objects.all()

    return render(
        request,
        "courses/course_list.html",
        {
            "courses": courses
        }
    )

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

@login_required
def add_course(request):
    if request.user.role != "admin":
        return redirect("home")
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        Course.objects.create(title=title, description=description, created_by=request.user)
        return redirect("courses")
    return render(request, 'courses/add_course.html')

@login_required
def enroll_student(request, course_id):
    if request.user.role != "admin":
        return redirect("home")
    course = get_object_or_404(Course, id=course_id)
    students = CustomUser.objects.filter(role='student')
    if request.method == "POST":
        student_id = request.POST.get("student")
        student = CustomUser.objects.get(id=student_id)
        course.assigned_students.add(student)
        return redirect("courses")
    return render(
        request, 
        'courses/enroll_student.html', 
        {
            'course': course, 'students' : students
        })

@login_required
def self_enroll(request, course_id):

    if request.user.role != "student":
        return redirect("home")

    course = get_object_or_404(
        Course,
        id=course_id
    )

    already_requested = EnrollmentRequest.objects.filter(
        student=request.user,
        course=course
    ).exists()

    if not already_requested:

        EnrollmentRequest.objects.create(
            student=request.user,
            course=course
        )

    return redirect("courses")

@login_required
def approve_enrollment(request, request_id):

    if request.user.role != "admin":
        return redirect("home")

    enrollment_request = get_object_or_404(
        EnrollmentRequest,
        id=request_id
    )

    enrollment_request.course.assigned_students.add(
        enrollment_request.student
    )

    enrollment_request.approved = True

    enrollment_request.save()

    return redirect("admin_dashboard")

@login_required
def watch_video(request, video_id):
    video = get_object_or_404(CourseVideo, id=video_id)
    course = video.course
    if request.user.role == "student":
        if request.user not in course.assigned_students.all():
            return redirect("courses")
    return render(request, 'courses/watch_video.html', {'video': video})