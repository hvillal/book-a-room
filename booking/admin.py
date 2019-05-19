from django.contrib import admin
from .models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    readonly_fields = ('created', )
    list_display = ('room', 'check_in', 'check_out', 'guest', )
    list_filter = ('room', 'guest', )
    date_hierarchy = 'check_in'


admin.site.register(Reservation, ReservationAdmin)
