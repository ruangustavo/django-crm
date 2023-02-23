from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ProductForm, SaleForm
from .models import Product, Sale
from .utils import format_currency


class HomeView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products_list"

    def get_enterprise_invoce(self):
        sales_invoice_obj = Sale.objects.aggregate(Sum("total_price"))
        sales_invoice = sales_invoice_obj["total_price__sum"]

        if sales_invoice is None:
            sales_invoice = 0

        return format_currency(sales_invoice)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sales_invoice"] = self.get_enterprise_invoce()
        return context


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

    def form_valid(self, form):
        product = Product.objects.filter(name=form.cleaned_data["name"]).first()

        if product is None:
            return super().form_valid(form)

        product.stock_quantity += form.cleaned_data["stock_quantity"]
        product.save()
        return super().form_valid(form)


class SaleView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = "sale.html"
    success_url = reverse_lazy("enterprise:home")

    def form_valid(self, form):
        sale = form.save(commit=False)
        sale.total_price = sale.product.price * sale.quantity
        sale.save()
        product = sale.product

        if sale.quantity > product.stock_quantity:
            return self.form_invalid(form)

        product.stock_quantity -= sale.quantity
        product.save()
        return super().form_valid(form)
