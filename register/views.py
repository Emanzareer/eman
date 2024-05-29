from django.shortcuts import render,redirect
from .forms  import *
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import auth
from django.contrib import messages
from .filters import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, render



@login_required(login_url='login')
def courses(request):
    courses=Courses.objects.all() 
    searchFilter=CourseFilter(request.POST,queryset=courses)
    courses=searchFilter.qs
    
    context={
        'courses':courses,
        'searchFilter':searchFilter,
    }
    return render(request,"register/courses.html",context)

@login_required(login_url='login')
def news(request):
    news=News.objects.all()
    context={
        "news":news
    }
    return render(request,"register/news.html",context)

@login_required(login_url='login')
def view(request, pk):
    course = get_object_or_404(Courses, id=pk)
    studentReg = StudentsReg.objects.filter(courseId=course).count()
    context = {
        'course': course,
        'studentReg':studentReg
    }
    return render(request, 'register/view.html', context)
 

@login_required(login_url='login')
def studentsReg(request,pk):
    student = Students.objects.get(id=pk)
    registrations = StudentsReg.objects.filter(studentId=pk)
    courses = []
    for reg in registrations:
        course = reg.courseId
        if course and course.scheduleId:
            courses.append({
                'name': course.name,
                'description': course.description,
                'instructor': course.instructor,
                'roomNo': course.scheduleId.roomNo,
                'days': ', '.join([day.name for day in course.scheduleId.days.all()]),
                'startTime': course.scheduleId.startTime.strftime('%H:%M'),
                'endTime': course.scheduleId.endTime.strftime('%H:%M')
            })
    context = {
        'student_name': student,
        'courses': courses
    }
    return render(request, 'register/studentsReg.html', context)

 
def create(request):
    form=createNewUser()
    if request.method=='POST':
        form=createNewUser(request.POST)
        if form.is_valid():  
            user=form.save(commit=False)
            user.password = make_password(form.cleaned_data['password']) 
            form.save()
            return redirect('login')
    else:
       form=createNewUser()
    return render(request,'register/create.html',{'form': form})


def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('news')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'register/login.html')

@login_required(login_url='login')
def registerCourse(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    student = request.user.student
    if StudentsReg.objects.filter(studentId=student, courseId=course).exists():
        messages.warning(request, 'You are already registered for this course.')
    else:
        student_courses = StudentsReg.objects.filter(studentId=student)
        for reg in student_courses:
            if reg.courseId.scheduleId and course.scheduleId:
                if reg.courseId.scheduleId.days.filter(id__in=course.scheduleId.days.all()).exists() and (
                        (reg.courseId.scheduleId.startTime <= course.scheduleId.startTime <= reg.courseId.scheduleId.endTime) or
                        (reg.courseId.scheduleId.startTime <= course.scheduleId.endTime <= reg.courseId.scheduleId.endTime)):
                    messages.error(request, 'There is a schedule conflict with another course.')
                    return redirect('view', pk=course_id)
        StudentsReg.objects.create(courseId=course, studentId=student)
        messages.success(request, 'You have successfully registered for the course.')

    return redirect('view', pk=course_id)



@login_required(login_url='login')  
def userLogout(request):
    logout(request)
    return redirect ('login')


