from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Customer, Order

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control mb-3 focus-ring text-decoration-none border'
            field.widget.attrs['style'] = '--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'
            field.widget.attrs['placeholder'] = field.label

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'}))

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'quantity', 'category',
            'height_cm', 'width_cm', 'material', 'finish', 'date_of_delivery',
            'image', 'imageuno', 'imagedos', 'imagetres'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'height_cm': forms.NumberInput(attrs={'class': 'form-control'}),
            'width_cm': forms.NumberInput(attrs={'class': 'form-control'}),
            'material': forms.Select(attrs={'class': 'form-control'}),
            'finish': forms.Select(attrs={'class': 'form-control'}),
            'date_of_delivery': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'imageuno': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'imagedos': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'imagetres': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'offer', 'offer_price', 'quantity',
            'category', 'height_cm', 'width_cm', 'material', 'finish', 'date_of_delivery',
            'image', 'imageuno', 'imagedos', 'imagetres'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'offer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'offer_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'height_cm': forms.NumberInput(attrs={'class': 'form-control'}),
            'width_cm': forms.NumberInput(attrs={'class': 'form-control'}),
            'material': forms.Select(attrs={'class': 'form-control'}),
            'date_of_delivery': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'imageuno': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'imagedos': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'imagetres': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        offer = cleaned_data.get('offer')
        offer_price = cleaned_data.get('offer_price')
        price = cleaned_data.get('price')

        if offer:
            if offer_price is None:
                self.add_error('offer_price', 'Debes especificar un precio de oferta.')
            elif offer_price >= price:
                self.add_error('offer_price', 'El precio de oferta debe ser menor que el precio original.')
        return cleaned_data
    
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'email', 'address', 'referencias', 'date_of_birth', 'zip_code', 'state', 'municipality']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'referencias': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),  # Añadido el widget para 'state'
            'municipality': forms.TextInput(attrs={'class': 'form-control'}),  # Añadido el widget para 'municipality'
        }
        
class OrderUpdateForm(forms.ModelForm):
    estimated_delivery = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Order
        fields = ['status', 'estimated_delivery']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }