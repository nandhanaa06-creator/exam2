from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image', 'category']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name',
                'style': 'padding:8px; font-size:14px;'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price',
                'style': 'padding:8px; font-size:14px;'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description',
                'rows': 3,
                'style': 'padding:8px; font-size:14px; resize:none;'
            }),

            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'style': 'padding:6px; font-size:14px;'
            }),

            'category': forms.Select(attrs={
                'class': 'form-select',
                'style': 'padding:8px; font-size:14px;'
            }),
        }
