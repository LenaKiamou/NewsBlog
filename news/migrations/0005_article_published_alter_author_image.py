# Generated by Django 4.0.3 on 2022-03-22 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_author_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='author',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='news/static/images/'),
        ),
    ]