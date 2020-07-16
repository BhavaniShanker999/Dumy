from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class create_order_form(ModelForm):
    class Meta:
        model= order_model
        fields='__all__'


class CustomerForm(ModelForm):
	class Meta:
		model = customer_model
		fields = '__all__'
		exclude = ['user']

class add_product_form(ModelForm):
    class Meta:
        model=Product_model
        fields='__all__'
        

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
