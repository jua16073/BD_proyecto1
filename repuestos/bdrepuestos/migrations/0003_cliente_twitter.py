# Generated by Django 2.0.2 on 2018-03-22 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bdrepuestos', '0002_auto_20180322_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='twitter',
            field=models.CharField(default='idolMariya', max_length=40),
            preserve_default=False,
        ),
    ]