# Generated by Django 5.2 on 2025-05-07 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Questions', '0002_alter_question_inputs_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='deadline',
            field=models.DateTimeField(),
        ),
    ]
