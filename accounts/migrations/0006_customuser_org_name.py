# Generated by Django 5.0.4 on 2024-05-31 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_delete_userprofile_customuser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='org_name',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]