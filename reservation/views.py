from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import ModelViewSet

from .filters import TableFilter
from .models import Table, Reservation
from .serializers import TableSerializer, ReservationSerializer


class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TableFilter

    # def get_permissions(self):
    #     """Получение прав для действий."""
    #     if self.action in ['create', 'destroy', 'update', 'partial_update']:
    #         return [IsAuthenticated()]
    #     return []


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    # def get_permissions(self):
    #     """Получение прав для действий."""
    #     if self.action in ['update', 'partial_update']:
    #         return [IsAuthenticated()]
    #     return []
