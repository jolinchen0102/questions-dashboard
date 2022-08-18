import django_tables2 as tables
from .models import Question

class QuestionTable(tables.Table):
    class Meta:
        model = Question
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", )