# Generated by Django 4.2.1 on 2023-05-13 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweet',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='tweet',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
    ]
