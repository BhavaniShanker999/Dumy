from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class customer_model(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=30,null=True)
    phone=models.IntegerField(null=True)
    mail=models.EmailField()
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    address=models.CharField(max_length=500,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class tag_model(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Product_model(models.Model):
    CATEGORY = (
            ('Astro','Astro'),
            ('Amazon','Amazon'),
			('Mobiles', 'Mobiles'),
			('Laptops', 'Laptops'),
			('Tabs', 'Tabs'),
			) 

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    tags=models.ManyToManyField(tag_model)

    def __str__(self):
        return self.name



    
    

    

    
class order_model(models.Model):
    STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)
    customer_mod=models.ForeignKey(customer_model,null=True,on_delete=models.SET_NULL)
    products_mod=models.ForeignKey(Product_model,null=True,on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    def __str__(self):
        return self.products_mod.name

