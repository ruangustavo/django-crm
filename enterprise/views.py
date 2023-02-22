from django.views import generic

from .models import Product


class HomeView(generic.ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products_list"
