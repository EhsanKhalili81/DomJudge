# Generated by Django 5.2 on 2025-05-07 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Questions', '0003_alter_question_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='language',
            field=models.CharField(choices=[('0', 'python'), ('1', 'c++'), ('2', 'c#'), ('3', 'java')], max_length=10),
        ),
    ]
