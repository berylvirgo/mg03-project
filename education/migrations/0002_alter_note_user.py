# Generated by Django 4.0 on 2021-12-22 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('education', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
    ]
