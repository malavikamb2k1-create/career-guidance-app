
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('colleges/', views.college_list, name='college_list'),
    path('aptitude-test/', views.aptitude_test, name='aptitude_test'),
    path('result/', views.result, name='result'),
]

