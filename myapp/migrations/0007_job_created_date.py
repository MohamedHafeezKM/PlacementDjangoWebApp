# Generated by Django 4.2.6 on 2023-12-15 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_studentprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]