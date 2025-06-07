from django.apps import AppConfig

class ReportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reports'

    def ready(self):
        from .models import ReportSection
        sections = [
            {'code': 'sales', 'name': 'مبيعات'},
            {'code': 'finance', 'name': 'مالية'},
            {'code': 'marketing', 'name': 'تسويق'},
            {'code': 'hr', 'name': 'الموارد البشرية'},
        ]
        for sec in sections:
            ReportSection.objects.get_or_create(code=sec['code'], defaults={'name': sec['name']})
