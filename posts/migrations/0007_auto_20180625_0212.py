# Generated by Django 2.0.6 on 2018-06-25 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20180625_0209'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Like'),
        ),
        migrations.AddField(
            model_name='post',
            name='unlike',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Unlike'),
        ),
        migrations.AlterField(
            model_name='post',
            name='message',
            field=models.TextField(default='', help_text='Your new message.', max_length=1500, verbose_name='Message'),
        ),
    ]
