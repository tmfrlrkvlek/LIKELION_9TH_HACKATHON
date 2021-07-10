from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Book)
admin.site.register(Room)
admin.site.register(Qna)
admin.site.register(File)
admin.site.register(Comment)