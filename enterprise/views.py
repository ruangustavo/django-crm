from django.db.models import Sum
from django.shortcuts import redirect
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

    def is_product_existing(self, form):
        product = Product.objects.filter(
            name=form["name"],
            price=form["price"],
        )

        return product.exists()

    def update_product_stock(self, form):
        product = Product.objects.get(
            name=form["name"],
            price=form["price"],
        )

        new_stock_quantity = int(form["stock_quantity"])
        product.stock_quantity += new_stock_quantity
        product.save()

    def form_valid(self, form):
        if self.is_product_existing(self.request.POST):
            self.update_product_stock(self.request.POST)
            return redirect(self.success_url)

        return super().form_valid(form)


class SaleView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = "sale.html"
    success_url = reverse_lazy("enterprise:home")

    def form_valid(self, form):
        sale = form.save(commit=False)
        product = sale.product

        if sale.quantity > product.stock_quantity:
            return self.form_invalid(form)

        self.update_product_stock_quantity(sale, product)
        return super().form_valid(form)

    def update_product_stock_quantity(self, sale, product):
        product.stock_quantity -= sale.quantity
        product.save()
