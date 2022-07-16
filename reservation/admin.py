from django.contrib import admin

from reservation.models import TypeOfTable, Table, Client, Reservation

admin.site.register(TypeOfTable)

admin.site.register(Table)

admin.site.register(Client)

admin.site.register(Reservation)
