# Generated by Django 4.1.2 on 2022-12-28 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_transferfunction_latex_expression'),
    ]

    operations = [
        migrations.RenameField(
            model_name='function',
            old_name='optimal_result',
            new_name='optimal',
        ),
    ]
