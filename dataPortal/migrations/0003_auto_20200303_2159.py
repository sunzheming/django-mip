# Generated by Django 3.0.3 on 2020-03-03 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataPortal', '0002_auto_20200303_0712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapdata',
            name='data_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='mapdata',
            name='data_url',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mapdata',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='mapdata',
            name='latitude',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='mapdata',
            name='longtitude',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='mapdata',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mapdata',
            name='user_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
