# Generated by Django 4.2.7 on 2023-12-05 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/blog/'),
        ),
        migrations.AlterField(
            model_name='article',
            name='publication',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='published', max_length=10),
        ),
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.CharField(db_index=True, max_length=100, unique=True),
        ),
    ]
