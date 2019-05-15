# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from transliterate import translit
import os
from django.core.cache import cache
import glob

VARS_OF_COUPONS = {
    "_oop_" : 10,
}

ORDER_STATUS_CHOICES = (
	('Accepted in processing', 'Accepted in processing'),
	('Performing', 'Performing'),
	('Paid', 'Paid')
)

class Category(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_slug(self):
        return self.slug

    def save(self, *args, **kwargs):
        try:
            self.slug = translit(self.name.lower(),reversed = True)
        except:
            self.slug = self.name.lower()
        return super(Category, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('category_detail',kwargs={'category_slug':self.slug})

"""
def pre_save_category_slug(sender, instance, *args, **kwargs):
	if not instance.slug:
		slug = slugify(translit(instance.name,reversed=True))
		instance.slug = slug

pre_save.connect(pre_save_category_slug, sender=Category)
"""

class Brand(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


def imagefolder(instance,filename:str):
    filename = instance.slug + '.' + filename.split('.')[1]
    return f"{instance.slug}/{filename}"


class ProductManager(models.Manager):
    def all(self,*args,**kwargs):
        return super(ProductManager,self).get_queryset().filter(available = True)
    

class Product(models.Model):
    category = models.ForeignKey(Category,null=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(Brand,null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=60)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to = imagefolder)
    price = models.DecimalField(max_digits=9,decimal_places=2,default = 0.00)
    available = models.BooleanField(default=True)
    count_in_stock = models.PositiveIntegerField(default=1)
    objects = ProductManager()

    def __str__(self):
        return self.title
    
    def get_image_info(self):
        return self.image
    
    def get_url(self):
        return reverse('product_detail',kwargs={'product_slug':self.slug})


class CartItem(models.Model):
    product = models.ForeignKey(Product,null = True, on_delete=models.SET_NULL)
    count = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Cart item for product - {product.title}"


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    final_price = models.DecimalField(max_digits=9,decimal_places=2,default = 0.00)
    is_sale = models.BooleanField(default=False)
    price_before_sale = models.DecimalField(max_digits=9,decimal_places=2,default = 0.00)

    def __str__(self):
        return f"{self.id}"

    def define_sale(self, coupon_for_sale: str):
        if coupon_for_sale in VARS_OF_COUPONS:
            self.final_price %= VARS_OF_COUPONS[coupon_for_sale]


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, on_delete=models.SET_NULL)
    items = models.ForeignKey(Cart,null=True, on_delete=models.SET_NULL)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    buying_type = models.CharField(max_length=40, choices=(('User pickup', 'User pickup'), 
		('Delivery', 'Delivery')), default='User pickup')
    date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField()
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])
    
    def __str__(self):
        return f"Order №{str(self.id)}"
        
class ShopCharacteristic(models.Model):
    total_money = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    total_usage_of_coupons = models.PositiveIntegerField(default=0)
    save_id = models.PositiveIntegerField(default=1)

class Coupon(models.Model):
    name = models.CharField(max_length = 40)
    coupon_sale = models.DecimalField(decimal_places = 2,max_digits = 4)
### добавить модель для купонов и добавить поле в product для количества на складе