# Generated by Django 4.2.7 on 2023-12-05 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='company',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
