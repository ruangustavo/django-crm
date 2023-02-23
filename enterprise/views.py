from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ProductForm
from .models import Product


class HomeView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products_list"


class ProductUpdateView(UpdateView):
    model = Product
    template_name = "product_update.html"
    form_class = ProductForm
    success_url = reverse_lazy("enterprise:home")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "product_delete.html"
    success_url = reverse_lazy("enterprise:home")
    context_object_name = "product"


class StockView(CreateView):
    model = Product
    template_name = "stock.html"
    form_class = ProductForm
    success_url = reverse_lazy("enterprise:home")
