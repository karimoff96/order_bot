from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.BigIntegerField(default=0, unique=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    price = models.IntegerField(default=0, blank=True, null=True)
    image1 = models.ImageField(upload_to='media', max_length=100, blank=True, null=True)
    image2 = models.ImageField(upload_to='media', max_length=100, blank=True, null=True)
    image3 = models.ImageField(upload_to='media', max_length=100, blank=True, null=True)
    image4 = models.ImageField(upload_to='media', max_length=100, blank=True, null=True)
    image5 = models.ImageField(upload_to='media', max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    step = models.IntegerField(default=0, blank=True, null=True)
    date = models.CharField(max_length=50, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    available_sizes = models.CharField(max_length=200, blank=True, null=True)
    available_amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    discount = models.IntegerField(default=0, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

