from django import forms
from .models import QuestionModel

class QuizForm(forms.ModelForm):
    class Meta:
        model = QuestionModel
        fields = ["name","a","b","c","d","answer"]