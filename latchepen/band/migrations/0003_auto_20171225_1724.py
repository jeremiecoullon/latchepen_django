# Generated by Django 2.0 on 2017-12-25 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('band', '0002_auto_20171225_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gig',
            name='preview_date_admin',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='date'),
        ),
    ]
