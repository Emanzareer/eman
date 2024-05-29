from django.urls import path
from . import views
urlpatterns = [
    path('courses/',views.courses,name='courses'),
    path('studentsReg/<str:pk>',views.studentsReg,name='studentsReg'),
    path('create/',views.create,name='create'),
    path('userLogin/',views.userLogin,name='login'),
    path('userLogout/',views.userLogout,name='userLogout'),
    path('view/<int:pk>',views.view,name='view'),
    path('registerCourse/<int:course_id>',views.registerCourse,name='registerCourse'),
    path('',views.news,name='news'),
]
