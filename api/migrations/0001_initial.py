# Generated by Django 5.0.3 on 2024-03-22 09:59

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
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
                ("order_date", models.DateTimeField(auto_now_add=True)),
                ("customer_name", models.CharField(max_length=100)),
                ("status", models.CharField(default="Pending", max_length=100)),
                (
                    "products",
                    models.ManyToManyField(related_name="orders", to="api.product"),
                ),
            ],
        ),
    ]
