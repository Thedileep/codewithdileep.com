# Generated by Django 4.2.3 on 2023-07-24 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easylearn', '0004_rename_full_name_admissionform_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='admissionform',
            name='country_state',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='admissionform',
            name='district',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='admissionform',
            name='pin',
            field=models.CharField(default='', max_length=10),
        ),
    ]