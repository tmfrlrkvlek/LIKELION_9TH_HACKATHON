from django.db import models
from django.contrib.auth.models import User
from django.db.models.enums import IntegerChoices
from django.db.models.fields import CharField, IntegerField
from django.db.models.fields.related import OneToOneField

# Create your models here.
class Profile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    point = IntegerField(default=0)
    nickname = CharField(max_length=45)
    def __str__(self):
        return self.user.username