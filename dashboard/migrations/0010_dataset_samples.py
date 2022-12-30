# Generated by Django 4.1.3 on 2022-12-30 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_rename_optimal_result_function_optimal'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='samples',
            field=models.IntegerField(default=1, help_text='Number of samples of the dataset', verbose_name='Samples'),
        ),
    ]