# Generated by Django 4.1.4 on 2023-03-09 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_profile_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.CharField(max_length=100, null=True, verbose_name='Автор'),
        ),
    ]
