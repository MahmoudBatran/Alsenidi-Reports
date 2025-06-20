# Generated by Django 5.1.4 on 2025-05-29 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('report_file', models.FileField(upload_to='reports/')),
                ('section', models.CharField(choices=[('sales', 'مبيعات'), ('inventory', 'مخزون'), ('customers', 'عملاء'), ('finance', 'ماليات'), ('marketing', 'تسويق')], max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
