# Generated by Django 2.0.2 on 2018-04-06 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bdrepuestos', '0010_campoadicional_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='foraneo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdrepuestos.Cliente'),
        ),
    ]