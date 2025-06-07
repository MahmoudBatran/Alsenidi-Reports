from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'report_file', 'section', 'description']
        labels = {
            'title': 'عنوان التقرير',
            'report_file': 'ملف التقرير',
            'section': 'القسم',
            'description': 'الوصف',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
