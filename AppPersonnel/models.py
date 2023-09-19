import datetime
from django.db import models




class Grade(models.Model):
    designation = models.CharField(max_length=255)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.designation


class Service(models.Model):
    designation = models.CharField(max_length=255)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.designation


class Fonction(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    designation = models.CharField(max_length=255)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service}-{self.designation}"




