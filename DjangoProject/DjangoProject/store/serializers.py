from rest_framework import serializers
from .models import Book, Author, Publisher, User, Order, Cart, OrderedItem
from django.contrib.auth.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_check = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_check')

    def validate(self, data):
        if data['password'] != data['password_check']:
            raise serializers.ValidationError({"password_check": "Паролі не співпадають"})
        return data

    def create(self, validated_data):
        validated_data.pop('password_check')
        return User.objects.create_user(**validated_data)

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'price', 'author', 'publisher', 'genre']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class CartSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source='book.name', read_only=True)
    book_price = serializers.DecimalField(source='book.price', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'book', 'book_name', 'book_price', 'amount', 'total_price']

    def get_total_price(self, obj):
        return obj.amount * obj.book.price


class OrderedItemSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source='book.name', read_only=True)
    book_price = serializers.DecimalField(source='book.price', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderedItem
        fields = ['id', 'order', 'book', 'book_name', 'book_price', 'amount', 'total_price']

    def get_total_price(self, obj):
        return obj.amount * obj.book.price


class OrderSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    ordered_items = OrderedItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'user_name', 'added', 'ordered_items', 'total_amount']

    def get_total_amount(self, obj):
        return sum(item.amount for item in obj.ordered_items.all())

    def get_total_price(self, obj):
        return sum(item.amount * item.book.price for item in obj.ordered_items.all())