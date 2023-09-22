from django.urls import path
from .import views


urlpatterns=[
    path('', views.index, name="index"),
    path('account/login', views.loginUser, name="loginUser"),
    path('account/logout', views.logoutUser,name='logoutUser'),
    path('account/changepassword', views.changePassword, name="changePassword")
    
]