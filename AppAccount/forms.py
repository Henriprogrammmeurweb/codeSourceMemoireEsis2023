from django import forms


class FormLogin(forms.Form):
    email=forms.CharField(widget=forms.EmailInput(attrs={"class":'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control'}))