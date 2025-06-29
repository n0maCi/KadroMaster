# Generated by Django 5.1.7 on 2025-06-14 20:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesscontrol',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainApp.employees'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainApp.employees'),
        ),
        migrations.AlterField(
            model_name='timetraking',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainApp.employees'),
        ),
        migrations.AlterField(
            model_name='user',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MainApp.employees'),
        ),
    ]
