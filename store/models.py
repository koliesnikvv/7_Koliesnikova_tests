from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal



class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], default=Decimal('0.0'))
    authors = models.ManyToManyField(Author)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='books', null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, related_name='books', null=True, blank=True)
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.name}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['user', 'book']

    def __str__(self):
        return f"{self.amount} x {self.book.name} in {self.user.name}'s cart"


class OrderedItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ordered_items')
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.amount} x {self.book.name} in order {self.order.id}"