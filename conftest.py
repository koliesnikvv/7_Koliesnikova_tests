import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from store.models import Author, Publisher, Book
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username="user", password="qwerty")


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def sample_author():
    return Author.objects.create(name="Test Author")

@pytest.fixture
def sample_publisher():
    return Publisher.objects.create(name="Test Publisher")

@pytest.fixture
def sample_book(sample_author, sample_publisher):
    return Book.objects.create(
        name="Test Book",
        price=29.99,
        author=sample_author,
        publisher=sample_publisher,
        genre="Fiction"
    )


