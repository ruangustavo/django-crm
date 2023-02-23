from django import forms

from .models import Product


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
                attrs={"placeholder": "Digite o preço do produto...", type: "number"}
            ),
            "stock_quantity": forms.NumberInput(
                attrs={
                    "placeholder": "Digite a quantidade em estoque...",
                    type: "number",
                }
            ),
        }
