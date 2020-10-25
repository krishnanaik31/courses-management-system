from django.urls import path, include
from myapp import views

app_name = 'myapp'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'<int:top_no>/', views.detail, name='detail'),
    path(r'courses/', views.courses, name='courses'),
    path(r'place_order/', views.place_order, name='place_order'),
    path(r'courses/<int:course_id>/', views.coursedetail, name='course_detail'),
    path(r'login/', views.user_login, name='login'),
    path(r'logout/', views.user_logout, name='logout'),
    path(r'my_account/', views.myaccount, name='my_account'),
    path(r'register/', views.register, name='register')
]
