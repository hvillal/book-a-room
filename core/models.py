from django.db import models


class RoomType(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    capacity = models.SmallIntegerField(verbose_name='Capacidad (personas)')

    class Meta:
        verbose_name = 'Tipo de habitación'
        verbose_name_plural = 'Tipos de habitaciones'

    def __str__(self):
        return self.name


class RoomFacility(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Equipamiento de la habitación'
        verbose_name_plural = 'Equipamientos de las habitaciones'

    def __str__(self):
        return self.name


class RoomStatus(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Estado de la habitación'
        verbose_name_plural = 'Estados de las habitaciones'

    def __str__(self):
        return self.name


class Room(models.Model):
    number = models.SmallIntegerField(verbose_name='Número de habitación', unique=True)
    type = models.ForeignKey(RoomType,
                             verbose_name='Tipo de habitación',
                             related_name='room_type',
                             on_delete=models.CASCADE)
    facilities = models.ManyToManyField(RoomFacility, verbose_name='Equipamiento', related_name='room_facilities')
    status = models.ForeignKey(RoomStatus,
                               verbose_name='Estado de la habitación',
                               related_name='room_status',
                               on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Precio')

    class Meta:
        verbose_name = 'Habitación'
        verbose_name_plural = 'Habitaciones'

    def __str__(self):
        return 'Habitación ' + str(self.number)
