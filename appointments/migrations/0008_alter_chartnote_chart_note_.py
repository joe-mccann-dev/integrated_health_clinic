# Generated by Django 5.0.7 on 2024-08-15 20:52

import django_quill.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0007_alter_chartnote_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chartnote',
            name='chart_note',
            field=django_quill.fields.QuillField(),
        ),
    ]
