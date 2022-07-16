from django.db import models


class OrderStatusChoices(models.TextChoices):
    """Статусы заказов."""

    RESERVED = 'Reserved', 'Зарезервирован'
    WAIT = 'Wait', 'Ожидает подтверждения'


class TypeOfTable(models.Model):
    table_type = models.CharField(max_length=20, verbose_name='Вид столика')

    def __str__(self):
        return self.table_type

    class Meta:
        verbose_name = 'Вид столика'
        verbose_name_plural = 'Виды столов'


class Table(models.Model):
    table_number = models.SmallIntegerField(primary_key=True, verbose_name='Номер стола')
    number_of_seats = models.SmallIntegerField(verbose_name='Количество мест')
    price = models.FloatField(verbose_name='Цена')
    type_id = models.ForeignKey(TypeOfTable, on_delete=models.CASCADE)

    def __str__(self):
        return f'Столик номер: {self.table_number}'

    class Meta:
        verbose_name = 'Столик'
        verbose_name_plural = 'Столики'


class Client(models.Model):
    email = models.EmailField(verbose_name='Электронная почта')
    phone = models.CharField(max_length=15, verbose_name='Номер телефона')

    def __str__(self):
        return f'Клиент номер: {self.pk}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    table = models.OneToOneField(Table, on_delete=models.CASCADE)
    status = models.TextField(
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.WAIT
    )

    def __str__(self):
        return f'Бронь номер: {self.pk}'

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
