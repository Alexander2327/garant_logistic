import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from model_bakery import baker

from reservation.models import Table, Reservation, TypeOfTable


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def tabletype():
    return TypeOfTable.objects.create(table_type='Комната')


@pytest.fixture
def table_factory():
    def factory(*args, **kwargs):
        return baker.make(Table, *args, **kwargs)

    return factory


@pytest.fixture
def reservation_factory():
    def factory(*args, **kwargs):
        return baker.make(Reservation, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_list_tables(api_client, table_factory):
    table_factory(_quantity=3)
    url = reverse('tables-list')
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.django_db
def test_table_filter_id(api_client, table_factory):
    course = table_factory(table_number=10, number_of_seats=5, price=4000)
    url = reverse('tables-list')
    response = api_client.get(url, {'number_of_seats': course.number_of_seats,
                                    'price_min': 3000,
                                    'price_max': 6000})
    data = response.json()
    assert response.status_code == 200
    assert data[0]['number_of_seats'] == course.number_of_seats
    assert data[0]['price'] >= 3000
    assert data[0]['price'] <= 6000


@pytest.mark.django_db
def test_create_table(api_client, tabletype):
    count = Table.objects.count()
    url = reverse('tables-list')
    table_data = {'table_number': 10,
                  'number_of_seats': 4,
                  'price': 3000,
                  'type_id': tabletype.id
                  }
    response = api_client.post(url, data=table_data)
    assert response.status_code == 201
    assert Table.objects.count() == count + 1
    assert api_client.get(url, table_data)


@pytest.mark.django_db
def test_update_table(api_client, table_factory):
    table = table_factory()
    old_table_price = table.price
    url = reverse('tables-detail', kwargs={'pk': table.table_number})
    table_data = {'price': 1000,
                  }
    response = api_client.patch(url, data=table_data)
    data = response.json()
    assert response.status_code == 200
    assert data['price'] == 1000
    assert old_table_price != data['price']


@pytest.mark.django_db
def test_delete_reservation(api_client, reservation_factory):
    reservation = reservation_factory()
    url = reverse('reservation-detail', kwargs={'pk': reservation.id})
    response = api_client.delete(url)
    assert response.status_code == 204
    response = api_client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_reservation(api_client, reservation_factory):
    reservation = reservation_factory()
    old_reservation_status = reservation.status
    url = reverse('reservation-detail', kwargs={'pk': reservation.id})
    reservation_data = {'status': 'Reserved',
                        }
    response = api_client.patch(url, data=reservation_data)
    data = response.json()
    assert response.status_code == 200
    assert data['status'] == 'Reserved'
    assert old_reservation_status != data['status']
