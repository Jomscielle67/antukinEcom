# Generated by Django 5.1.1 on 2024-10-09 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0004_profile_old_cart"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image_url",
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
