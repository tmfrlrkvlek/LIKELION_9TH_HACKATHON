from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField, CharField, DateTimeField, IntegerField, TextField
from django.db.models.fields.files import FileField
from django.db.models.fields.related import ForeignKey, OneToOneField
from account.models import Profile

# Create your models here.
class Book(models.Model):
    isbn = CharField(max_length=100)
    title = CharField(max_length=255)
    author = CharField(max_length=100)
    publisher = CharField(max_length=255)
    imageUrl = CharField(max_length=500, null=True)
    def __str__(self):
        return self.title

class Room(models.Model):
    book = OneToOneField(Book, on_delete=CASCADE)
    def __str__(self):
        return self.book.title

class Qna(models.Model):
    room = ForeignKey(Room, on_delete=CASCADE)
    title = CharField(max_length=500)
    writer = ForeignKey(Profile, on_delete=CASCADE)
    content = TextField()
    isfile = BooleanField(default=False)
    pubdate = DateTimeField(auto_now_add=True)
    chapter = IntegerField()
    page = IntegerField()
    qnum = CharField(max_length=100, null=True)
    selected = BooleanField(default=False)
    def __str__(self):
        return self.room.book.title + " - " + self.title
    
class File(models.Model):
    profile = ForeignKey(Profile, on_delete=CASCADE)
    qna = ForeignKey(Qna, on_delete=CASCADE)
    order = IntegerField(default=1)
    filename = FileField()
    def __str__(self):
        return self.filename.url

class Comment(models.Model):
    qna = ForeignKey(Qna, on_delete=CASCADE, null=True)
    writer = ForeignKey(Profile, on_delete=CASCADE)
    content = TextField()
    isfile = BooleanField(default=False)
    pubdate = DateTimeField(auto_now_add=True)
    parent = IntegerField()
    depth = IntegerField(default=1)
    selected = BooleanField(default=False)
    def __str__(self):
        return self.content


