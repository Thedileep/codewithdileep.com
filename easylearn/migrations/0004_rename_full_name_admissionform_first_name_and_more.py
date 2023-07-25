# Generated by Django 4.2.3 on 2023-07-24 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easylearn', '0003_alter_admissionform_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admissionform',
            old_name='full_name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='admissionform',
            name='last_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]