from django.forms import ModelForm
from .models import Question

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description', 'input_form', 'course']  # Specify fields to include in the form
