from django import forms

from .models import Product, Sale


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        labels = {
            "image": "Imagem",
            "name": "Nome",
            "price": "Preço",
            "stock_quantity": "Quantidade em estoque",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Digite o nome do produto..."}
            ),
            "price": forms.NumberInput(
                attrs={"placeholder": "Digite o preço do produto..."}
            ),
            "stock_quantity": forms.NumberInput(
                attrs={"placeholder": "Digite a quantidade em estoque..."}
            ),
        }


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ("product", "quantity")
        labels = {
            "product": "Produto",
            "quantity": "Quantidade",
        }
        widgets = {
            "product": forms.Select(attrs={"placeholder": "Selecione um produto..."}),
            "quantity": forms.NumberInput(
                attrs={
                    "placeholder": "Digite a quantidade que será vendida...",
                    type: "number",
                }
            ),
        }
