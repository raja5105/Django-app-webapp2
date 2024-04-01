from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    products = models.ManyToManyField(Product, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='Pending')
    payment_status = models.CharField(max_length=100, default='Pending')  # Payment status field
    transaction_id = models.CharField(max_length=255, null=True, blank=True)  # Transaction ID field

    def __str__(self):
        return f'Order {self.id} - {self.customer_name}'


