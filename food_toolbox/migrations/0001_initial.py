# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 15:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_text', models.CharField(max_length=200)),
                ('last_modified_date', models.DateField(verbose_name=b'last modified')),
                ('process_description', models.TextField()),
                ('cooking_temperature_celsius', models.IntegerField(blank=True)),
                ('preparation_time_minutes', models.IntegerField(blank=True)),
                ('presentation_image_link', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe_Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient_quantity', models.CharField(blank=True, max_length=100, null=True)),
                ('ingredient_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_toolbox.Ingredients_List')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_toolbox.Recipe')),
            ],
        ),
    ]