from django.db import models
from django.contrib.auth.models import User
from core.models import Room


class Reservation(models.Model):
    number = models.CharField(max_length=32, verbose_name='Localizador')
    guest = models.ForeignKey(User, verbose_name='Huésped', on_delete=models.CASCADE)
    check_in = models.DateField(verbose_name='Fecha ingreso')
    check_out = models.DateField(verbose_name='Fecha salida')
    room = models.ForeignKey(Room, verbose_name='Habitación', on_delete=models.CASCADE, related_name='room_reservation')
    card_number = models.CharField(max_length=19, verbose_name='Número de tarjeta')
    expiry_month = models.CharField(max_length=2, verbose_name='Mes expiración')
    expiry_year = models.CharField(max_length=2, verbose_name='Año expiración')
    comments = models.TextField(verbose_name='Comentarios', null=True, blank=True)
    total = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Total reserva')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha reserva')

    class Meta:
        verbose_name = 'Reserva'

    def total_nights(self):
        return (self.check_out - self.check_in).days

    def price_per_night(self):
        return self.total / self.total_nights()

    def __str__(self):
        return self.number
