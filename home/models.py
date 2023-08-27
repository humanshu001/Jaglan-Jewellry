from django.db import models
from django.contrib.auth.models import User
import datetime
import os

# Create your models here.
class AppointmentRequest(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.CharField(max_length=10,null=False, blank=False)
    preferred_date = models.DateField(null=False, blank=False)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name




def get_file_path(request, filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename= "%s%s" % (nowTime, original_filename)
    return os.path.join('uploads/', filename)

class Category(models.Model):
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=get_file_path, null=True, blank=False)
    description= models.TextField(max_length=500, null=False, blank=False)
    status= models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending= models.BooleanField(default=False, help_text="0=default, 1=Trending")
    meta_title= models.CharField(max_length=150, null=False, blank=False)
    meta_keywords= models.CharField(max_length=150, null=False, blank=False)
    meta_description= models.TextField(max_length=500, null=False, blank=False)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to=get_file_path, null=True, blank=False)
    small_description= models.CharField(max_length=250, null=False, blank=False)
    quantity= models.IntegerField(null=False, blank=False, default=1)
    description= models.TextField(max_length=1500, null=False, blank=False)
    original_price= models.FloatField(null=False, blank=False)
    selling_price= models.FloatField(null=False, blank=False)
    status= models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending= models.BooleanField(default=False, help_text="0=default, 1=Trending")
    tag = models.CharField(max_length=150, null=False, blank=False)
    meta_title= models.CharField(max_length=150, null=False, blank=False)
    meta_keywords= models.CharField(max_length=150, null=False, blank=False)
    meta_description= models.TextField(max_length=500, null=False, blank=False)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 
    
class Cart(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty= models.IntegerField(null=False, blank=False, default=1)
    created_at= models.DateTimeField(auto_now_add=True)



class Wishlist(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    firstname= models.CharField(max_length=150, null=False)
    lastname= models.CharField(max_length=150, null=False)
    email= models.CharField(max_length=150, null=False)
    phone= models.CharField(max_length=150, null=False)
    address= models.TextField(null=False)
    city= models.CharField(max_length=150, null=False)
    state= models.CharField(max_length=150, null=False)
    country= models.CharField(max_length=150, null=False)
    pin= models.CharField(max_length=150, null=False)
    total_price= models.FloatField(null=False)
    payment_mode= models.CharField(max_length=150, null=False)
    payment_id= models.CharField(max_length=150, null=True)
    orderstatuses= (
        ('Pending','Pending'),
        ('Dispatched','Dispatched'),
        ('Shipped','Shipped'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    status= models.CharField(max_length=150, choices=orderstatuses, default="Pending")
    message= models.TextField(null=True)
    tracking_no= models.CharField(max_length=150, null=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no) # type: ignore
    
class Orderitem(models.Model):
    order= models.ForeignKey(Order, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    price= models.FloatField(null=False)
    quantity= models.IntegerField(null=False)

    def __str__(self):
        return'{} {}'.format(self.order.id, self.order.tracking_no) # type: ignore
    
class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    phone= models.CharField(max_length=150, null=False)
    address= models.TextField(null=False)
    city= models.CharField(max_length=150, null=False)
    state= models.CharField(max_length=150, null=False)
    country= models.CharField(max_length=150, null=False)
    pin= models.CharField(max_length=150, null=False)
    created_at= models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.user.username



class Feedback(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    feedback= models.TextField(null=True, blank=False)


    def __str__(self):
        return self.user.username