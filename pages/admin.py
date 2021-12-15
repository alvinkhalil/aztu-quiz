from django.contrib import admin

from pages.models import QuestionModel, ResultsModel

# Register your models here.



admin.site.register(QuestionModel)
admin.site.register(ResultsModel)