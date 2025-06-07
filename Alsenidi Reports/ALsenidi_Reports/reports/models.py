from django.db import models
from django.contrib.auth.models import User

class ReportSection(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Report(models.Model):
    title = models.CharField(max_length=255)
    report_file = models.FileField(upload_to='reports/')
    section = models.ForeignKey(ReportSection, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SectionPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(ReportSection, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'section')

    def __str__(self):
        return f"{self.user.username} - {self.section.name}"
