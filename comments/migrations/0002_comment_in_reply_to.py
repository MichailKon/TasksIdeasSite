# Generated by Django 4.1.7 on 2023-03-16 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='in_reply_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.comment'),
        ),
    ]
