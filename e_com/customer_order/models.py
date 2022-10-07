from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, null=False)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


class Orders(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    placed_date = models.DateTimeField()

    def __str__(self):
        return f"{self.customer}-{self.product}"

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Orders.objects.filter(customer_id=customer_id).order_by('-placed_date')


