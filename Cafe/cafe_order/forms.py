from django import forms
from .models import Customer

class CustomerRegisterInForm(forms.ModelForm):
    customer_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Customer
        fields = ['customer_name_surname', 'customer_email', 'customer_password']

class CustomerLoginForm(forms.ModelForm):
    customer_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Customer
        fields = ['customer_email', 'customer_password']
        