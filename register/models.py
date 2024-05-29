from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Day(models.Model):
    name=models.CharField(max_length=90,null=True)
    def __str__(self):
        return self.name
    
class CourseSchedules(models.Model):
    days=models.ManyToManyField(Day)
    startTime=models.TimeField( auto_now_add=False,null=True)
    endTime=models.TimeField( auto_now_add=False,null=True)
    roomNo=models.CharField( max_length=50,null=True)
    
class Courses(models.Model):
    name=models.CharField( max_length=50,null=True)
    description=models.CharField( max_length=200,null=True)
    prerequisites=models.CharField( max_length=100,null=True)
    instructor=models.CharField( max_length=50,null=True)
    capacity=models.FloatField(null=True)
    scheduleId=models.ForeignKey(CourseSchedules, on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.name
    
class Students(models.Model):
    name=models.CharField( max_length=50,null=True)
    password=models.CharField( max_length=50,null=True)
    email=models.CharField( max_length=50,null=True)
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='student',null=True)
    def __str__(self):
        return self.name or self.user.username
    
class StudentsReg(models.Model):
    studentId=models.ForeignKey(Students, on_delete=models.SET_NULL,null=True)
    courseId=models.ForeignKey(Courses,on_delete=models.SET_NULL,null=True)
     
class News(models.Model):
    name=models.CharField( max_length=50,null=True)
    description=models.CharField( max_length=200,null=True)
    def __str__(self):
        return self.name
