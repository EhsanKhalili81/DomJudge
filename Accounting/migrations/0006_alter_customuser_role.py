# Generated by Django 5.2 on 2025-05-10 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounting', '0005_customuser_nationalcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('0', 'Teacher'), ('1', 'Student'), ('2', 'Contester')], default='student', max_length=7),
        ),
    ]
