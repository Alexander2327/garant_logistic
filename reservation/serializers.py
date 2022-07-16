from rest_framework import serializers

from .models import Table, TypeOfTable, Reservation, Client


class TypeOfTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfTable
        fields = ('table_type',)


class TableSerializer(serializers.ModelSerializer):
    type_id = TypeOfTableSerializer(read_only=True)

    class Meta:
        model = Table
        fields = ('table_number', 'number_of_seats', 'price', 'type_id')

    def create(self, validated_data):
        validated_data['type_id'] = TypeOfTable.objects.get(id=self.context['request'].data['type_id'])
        return super().create(validated_data)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'email', 'phone',)


class ReservationSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ('table', 'status', 'client')

    def create(self, validated_data):
        client = Client.objects.create(email=self.context['request'].query_params['email'],
                                       phone=self.context['request'].query_params['phone'])
        validated_data['client'] = Client.objects.get(id=client.id)
        return super().create(validated_data)
