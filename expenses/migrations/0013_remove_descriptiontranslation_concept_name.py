# Generated by Django 2.1.7 on 2019-04-12 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0012_descriptiontranslation_concept'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='descriptiontranslation',
            name='concept_name',
        ),
    ]