# Generated by Django 2.0 on 2018-01-24 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('band', '0010_auto_20171229_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='gig',
            name='jamboree',
            field=models.BooleanField(default=False),
        ),
    ]
