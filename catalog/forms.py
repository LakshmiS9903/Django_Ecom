from django import forms
from .models import ParentProduct, ChildProduct

class ParentProductForm(forms.ModelForm):
    class Meta:
        model = ParentProduct
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter parent product title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter parent product description', 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ChildProductForm(forms.ModelForm):
    class Meta:
        model = ChildProduct
        fields = ['parent', 'title', 'description', 'image', 'price']
        widgets = {
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'placeholder': 'Enter child product title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter child product description', 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter product price', 'class': 'form-control'}),
        }
