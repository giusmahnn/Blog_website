# Generated by Django 5.0.6 on 2024-05-24 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_liked_comment_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='value',
            field=models.CharField(default=False, max_length=10),
        ),
    ]
