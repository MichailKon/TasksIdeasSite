# Generated by Django 4.1.5 on 2023-03-09 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0024_alter_comment_options_alter_idea_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата комментария'),
        ),
        migrations.AlterField(
            model_name='idea',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата записи'),
        ),
    ]
