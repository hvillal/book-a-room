from django.views.generic import FormView
from .forms import DatesSelection


class HomePageView(FormView):
    """
    Página principal del buscador de habitaciones
    """
    form_class = DatesSelection
    template_name = 'core/home.html'
