# Generated by Django 4.2.6 on 2023-12-08 00:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0004_alter_report_reason"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="report",
            name="reporter",
        ),
    ]
