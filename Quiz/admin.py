from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(UserInfo)
admin.site.register(QuestionAnswer)
admin.site.register(QuizDetail)