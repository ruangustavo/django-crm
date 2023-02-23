from django.urls import path

from .views import HomeView, ProductDeleteView, ProductUpdateView, StockView

app_name = "enterprise"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("product/<int:pk>/update", ProductUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete", ProductDeleteView.as_view(), name="product_delete"),
    path("stock", StockView.as_view(), name="stock"),
]
