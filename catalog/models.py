from django.db import models
from django.db import models
from django.contrib.auth.models import User

class ParentProduct(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ChildProduct(models.Model):
    parent = models.ForeignKey(ParentProduct, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class WishList(models.Model):
    user = models.ForeignKey(User, related_name='wishlist_user', on_delete=models.CASCADE)
    child_product = models.ForeignKey(ChildProduct, related_name='child_product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.child_product.title} - {self.user.username}"
    

class AddToCart(models.Model):
    user = models.ForeignKey(User, related_name='add_to_cart_user', on_delete=models.CASCADE)
    child_product = models.ForeignKey(ChildProduct, related_name='add_to_cart_product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.child_product.title} - {self.user.username}"

    @property
    def total_price(self):
        # Calculate total price directly from the ChildProduct price
        return self.quantity * self.child_product.price