from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import Http404, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from core.models import Room
from .models import Reservation
from .forms import ReservationForm
from weasyprint import HTML
from django.template.loader import render_to_string
import datetime
import string
import random


class BookingPage(TemplateView):
    """
    Lista las habitaciones disponibles para las fechas seleccionadas en el home
    """
    template_name = 'booking/booking.html'

    def get(self, request, *args, **kwargs):
        if not all(key in request.GET for key in ['check_in', 'check_out']):
            return redirect('home')

        try:
            check_in = datetime.datetime.strptime(request.GET['check_in'], '%d-%m-%Y')
            check_out = datetime.datetime.strptime(request.GET['check_out'], '%d-%m-%Y')
            nights = (check_out - check_in).days
            if nights <= 0:
                raise ValueError
        except ValueError:
            return redirect('home')

        available_rooms = Room.objects.exclude(room_reservation__check_in__lte=check_out,
                                               room_reservation__check_out__gte=check_in)
        return render(request, self.template_name,
                      {
                          'rooms': available_rooms,
                          'check_in': request.GET['check_in'],
                          'check_out': request.GET['check_out'],
                          'nights': nights
                      })


class ReservationList(LoginRequiredMixin, ListView):
    """
    Lista todas las reservas del usuario
    """
    model = Reservation

    def get_queryset(self):
        queryset = super(ReservationList, self).get_queryset()
        return queryset.filter(guest=self.request.user)


class ReservationDetail(LoginRequiredMixin, DetailView):
    """
    Página para visualizar el detalle de la reserva
    """
    model = Reservation

    def get_queryset(self):
        queryset = super(ReservationDetail, self).get_queryset()
        return queryset.filter(guest=self.request.user)


class ReservationPage(LoginRequiredMixin, CreateView):
    """
    Página para crear la reserva de la habitación
    """
    model = Reservation
    form_class = ReservationForm

    def setup(self, request, *args, **kwargs):
        super(ReservationPage, self).setup(request, *args, **kwargs)
        room = get_object_or_404(Room, pk=self.kwargs['room_id'])

        try:
            check_in = datetime.datetime.strptime(self.kwargs['check_in'], '%d-%m-%Y')
            check_out = datetime.datetime.strptime(self.kwargs['check_out'], '%d-%m-%Y')
            nights = (check_out - check_in).days
            if nights <= 0:
                raise ValueError
        except:
            raise Http404('Error validando fechas')

        self.kwargs['room'] = room
        self.kwargs['check_in_dt'] = check_in
        self.kwargs['check_out_dt'] = check_out
        self.kwargs['nights'] = nights

    def get_context_data(self, **kwargs):
        context = super(ReservationPage, self).get_context_data(**kwargs)
        context['check_in'] = self.kwargs['check_in']
        context['check_out'] = self.kwargs['check_out']
        context['nights'] = self.kwargs['nights']
        context['room'] = self.kwargs['room']

        return context

    def form_valid(self, form):
        reservation = form.save(commit=False)
        reservation.number = reservation_number()
        reservation.room = self.kwargs['room']
        reservation.guest = self.request.user
        reservation.check_in = self.kwargs['check_in_dt']
        reservation.check_out = self.kwargs['check_out_dt']
        reservation.total = self.kwargs['room'].price * self.kwargs['nights']
        reservation.save()

        return redirect('booking:my_list')


class ReservationDetailPDF(LoginRequiredMixin, DetailView):
    """
    Página para visualizar el detalle de la reserva en PDF
    """
    model = Reservation
    template_name = 'booking/reservation_pdf.html'

    def get_queryset(self):
        queryset = super(ReservationDetailPDF, self).get_queryset()
        return queryset.filter(guest=self.request.user)

    def render_to_response(self, context, **response_kwargs):
        return render_to_pdf(self.template_name, context)


def render_to_pdf(template_name, context):
    """
    Función para generar PDF a partir de una página
    """
    html_string = render_to_string(template_name, context)

    html = HTML(string=html_string)
    result = html.write_pdf()

    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = 'filename=booking_pdf.pdf'

    return response


def reservation_number():
    """
    Generador de número de reserva

    :return: localizador
    """
    chars = string.ascii_letters + string.digits
    number = "".join(random.choice(chars) for _ in range(random.randint(8, 32)))

    return number
