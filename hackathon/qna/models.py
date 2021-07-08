from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField, CharField, DateTimeField, IntegerField, TextField
from django.db.models.fields.files import FileField
from django.db.models.fields.related import ForeignKey, OneToOneField
from account.models import Profile

# Create your models here.
class Book(models.Model):
    isbn = CharField(max_length=20)
    title = CharField(max_length=255)
    author = CharField(max_length=100)
    publisher = CharField(max_length=255)

class Room(models.Model):
    book = OneToOneField(Book, on_delete=CASCADE)

class Qna(models.Model):
    room = ForeignKey(Room, on_delete=CASCADE)
    title = CharField(max_length=500)
    writer = ForeignKey(Profile, on_delete=CASCADE)
    content = TextField()
    isfile = BooleanField(default=False)
    pubdate = DateTimeField(auto_now_add=True)
    chapter = IntegerField()
    page = IntegerField()
    qnum = CharField(max_length=100)
    
class File(models.Model):
    profile = ForeignKey(Profile, on_delete=CASCADE)
    qna = ForeignKey(Qna, on_delete=CASCADE)
    order = IntegerField(default=1)
    filename = FileField()

class Comment(models.Model):
    writer = ForeignKey(Profile, on_delete=CASCADE)
    content = TextField()
    isfile = BooleanField(default=False)
    pubdate = DateTimeField(auto_now_add=True)
    parent = IntegerField()
    depth = IntegerField(default=1)
    selected = BooleanField(default=False)


