
from django import forms
from .models import Watch, Order


class WatchForm(forms.ModelForm):

    class Meta:
        model = Watch
        fields = [
            'name',
            'price',
            'category',
            'description',
            'image',
            'stock',
            'is_featured',
            'is_active',
        ]

        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter watch description...'
            }),
        }




# Collect customer information and payment method during checkout
class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            'customer_name',
            'customer_phone',
            'customer_email',
            'delivery_address',
            'payment_method',
        ]

        widgets = {
            'customer_name': forms.TextInput(attrs={
                'placeholder': 'Enter your full name'
            }),

            'customer_phone': forms.TextInput(attrs={
                'placeholder': 'Enter your phone number'
            }),

            'customer_email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address'
            }),

            'delivery_address': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter your delivery address'
            }),

            'payment_method': forms.Select(),
        }

# Collect order identification details for customer order tracking
# Collect customer details for tracking their orders
class OrderTrackingForm(forms.Form):

    customer_name = forms.CharField(
        max_length=200,
        label='Full Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your full name'
        })
    )

    customer_phone = forms.CharField(
        max_length=20,
        label='Phone Number',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your phone number'
        })
    )