# Generated by Django 4.2.10 on 2024-06-02 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DataPoint",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(max_length=100)),
                ("value", models.FloatField()),
            ],
        ),
        migrations.DeleteModel(
            name="Grafico",
        ),
    ]
