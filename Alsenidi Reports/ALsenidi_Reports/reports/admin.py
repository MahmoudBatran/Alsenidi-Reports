from django.contrib import admin
from .models import Report, ReportSection, SectionPermission

admin.site.register(ReportSection)
admin.site.register(Report)
admin.site.register(SectionPermission)
