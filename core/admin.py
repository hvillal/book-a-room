from django.contrib import admin
from .models import RoomStatus, RoomFacility, RoomType, Room


class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', )
    ordering = ('capacity', )


class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'type', 'status', 'price', 'room_facilities')
    ordering = ('number', )
    list_filter = ('status', 'type', 'facilities', )

    def room_facilities(self, room):
        return ', '.join([facility.name for facility in room.facilities.all().order_by('name')])

    room_facilities.short_description = 'Características'


admin.site.register(RoomStatus)
admin.site.register(RoomFacility)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
