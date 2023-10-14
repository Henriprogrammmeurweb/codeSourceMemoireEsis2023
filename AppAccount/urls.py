from django.urls import path
from django.contrib.auth.views import (PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)
                                       
from .import views
from .import forms



urlpatterns=[
    path('', views.index, name="index"),
    path('account/login', views.loginUser, name="loginUser"),
    path('account/logout', views.logoutUser,name='logoutUser'),
    path('account/change-password', views.changePassword, name="changePassword"),
    path('appropos-de-nous', views.appropos, name="appropos"),

    #reinitialisation du mot de password utilisateur
    path('account/password_reset/', PasswordResetView.as_view(template_name='reset_password/password_reset.html', form_class=forms.Formpassword_reset),name='password_reset'),
    path('account/password_reset/done/',PasswordResetDoneView.as_view(template_name='reset_password/password_send_email.html'), name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name='reset_password/password_set_confirm.html', form_class=forms.FormSetPassword),name='password_reset_confirm'),
    path('account/reset/done/',PasswordResetCompleteView.as_view(template_name='reset_password/password_reset_complete.html'),name='password_reset_complete'),
    
]

