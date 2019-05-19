from django.urls import path
from .views import BookingPage, ReservationList, ReservationPage, ReservationDetail, ReservationDetailPDF

booking_patterns = ([
    # Lista habitaciones disponibles
    path('', BookingPage.as_view(), name='booking'),
    # Formulario para reserva
    path('reservation/<int:room_id>/<str:check_in>/<str:check_out>/', ReservationPage.as_view(), name='reservation'),
    # Lista mis reservas
    path('list/', ReservationList.as_view(), name='my_list'),
    # Detalle de una reserva
    path('detail/<int:pk>/', ReservationDetail.as_view(), name='detail'),
    # Vista PDF de una reserva
    path('pdf/<int:pk>/', ReservationDetailPDF.as_view(), name='pdf'),
], 'booking')
