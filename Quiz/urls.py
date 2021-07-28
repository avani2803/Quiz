from django.urls import path

from . import views

urlpatterns = [
    #Index Page
    path('',views.home,name='home'),

    #User Register
    path('register',views.register,name='register'),

    # User Register
    path('login',views.login,name='login'),

    #logout
    path('logout',views.Logout, name='logout'),

    # path('test',views.test),

    path('start/quiz',views.startQuiz, name='startQuiz'),
    path('submit', views.submitQuiz, name='submit'),
    path('about',views.about)

]