# Generated by Django 2.2.4 on 2019-08-02 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list',
            old_name='item',
            new_name='task',
        ),
    ]
