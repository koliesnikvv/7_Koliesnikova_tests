import pytest
from rest_framework import status
from django.urls import reverse
from store.models import Book

@pytest.mark.django_db
def test_get_books_list(api_client, sample_book):
    url = reverse('book-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0


@pytest.mark.django_db
def test_create_book_authenticated(auth_client, sample_author, sample_publisher):
    url = reverse('book-list')
    data = {
        "name": "New Book",
        "price": "19.99",
        "author": sample_author.id,
        "publisher": sample_publisher.id,
        "genre": "Adventure"
    }
    response = auth_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Book.objects.filter(name="New Book").exists()


@pytest.mark.django_db
def test_create_book_unauthenticated(api_client, sample_author, sample_publisher):
    url = reverse('book-list')
    data = {
        "name": "Unauthorized Book",
        "price": "10.00",
        "author": sample_author.id,
        "publisher": sample_publisher.id,
        "genre": "Drama"
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
def test_update_book(auth_client, sample_book, sample_author, sample_publisher):
    url = reverse('book-detail', args=[sample_book.id])
    data = data = {
        "name": "Updated Book",
        "price": "29.99",
        "author": sample_author.id,
        "publisher": sample_publisher.id,
        "genre": "Mystery"}
    response = auth_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    sample_book.refresh_from_db()
    assert sample_book.name == "Updated Book"


@pytest.mark.django_db
def test_delete_book(auth_client):
    url = reverse('book-detail', args=[999])
    response = auth_client.delete(url)
    assert response.status_code == 404
