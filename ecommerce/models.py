from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

# ---------------------
# CATEGORY (MOVE THIS ABOVE PRODUCT)
# ---------------------
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category/', blank=True, null=True)

    def __str__(self):
        return self.name


# ---------------------
# PRODUCT
# ---------------------
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    stock = models.PositiveIntegerField(default=0)  # <-- stock field added

    show_on_homepage = models.BooleanField(default=False)  # NEW FIELD


    def __str__(self):
        return self.name


# ---------------------
# CART ITEM
# ---------------------
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.user.username}"

    def total_price(self):
        return self.product.price * self.quantity


# ---------------------
# ORDER
# ---------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    def calculate_total(self):
        total = sum(item.total_price() for item in self.items.all())
        self.total_amount = total
        self.save()
        return total


# ---------------------
# ORDER ITEM
# ---------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"


# ---------------------
# USER PROFILE
# ---------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_image = models.ImageField(upload_to='profile_pics/', default='default.png')
    last_location = models.CharField(max_length=255, blank=True, null=True)  # NEW FIELD


    def __str__(self):
        return self.user.username



class Banner(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else f"Banner {self.id}"
