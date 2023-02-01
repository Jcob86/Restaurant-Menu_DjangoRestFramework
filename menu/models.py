from django.db import models
from django.core.validators import MinValueValidator


class Cart(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title'] 


class Dish(models.Model):
    title = models.CharField(max_length=255)
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT, related_name='dishes')
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    preparation_time = models.DurationField()
    added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    is_vegetarian = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.title} for Menu: {self.cart}'

    class Meta:
        ordering = ['title'] 