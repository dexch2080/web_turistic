# Generated by Django 4.1.3 on 2022-12-04 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0004_rename_touristiczone_tour'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='image',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='trending',
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='places/images/')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.tour')),
            ],
        ),
    ]
