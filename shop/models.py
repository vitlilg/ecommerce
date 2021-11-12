from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name_category = models.CharField(max_length=250, unique=True)
    slug_category = models.SlugField(max_length=250, unique=True)
    description_cateory = models.TextField(blank=True)
    image_category = models.ImageField(upload_to='category', blank=True)

    class Meta:
        ordering = ('name_category', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug_category])

    def __str__(self):
        return self.name_category


class Product(models.Model):
    name_product = models.CharField(max_length=250, unique=True)
    slug_product = models.SlugField(max_length=250, unique=True)
    description_product = models.TextField(blank=True)
    category_product = models.ForeignKey(Category, on_delete=models.CASCADE)
    price_product = models.DecimalField(max_digits=10, decimal_places=2)
    image_product = models.ImageField(upload_to='product', blank=True)
    stock_product = models.IntegerField()
    available_product = models.BooleanField(default=True)
    created_product = models.DateTimeField(auto_now_add=True)
    updated_product = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name_product', )
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def get_url(self):
        return reverse('product_detail', args=[self.category_product.slug_category, self.slug_product])

    def __str__(self):
        return self.name_product


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['date_added']
        db_table = 'Cart'

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.product.price_product * self.quantity

    def __str__(self):
        return self.product
