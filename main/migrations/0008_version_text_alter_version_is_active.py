# Generated by Django 4.2.7 on 2024-01-02 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_teaproduct_name_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='version',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='active version'),
        ),
    ]