from django.db import models

# Create your models here.

class Product(models.Model):
    CAT=((1,'Men'),(2,"Womens"),(3,"Kids"))
    name=models.CharField(max_length=30)
    price=models.FloatField()
    category=models.IntegerField(choices=CAT , verbose_name="category")
    description=models.CharField(max_length=300,verbose_name="Details")
    is_active=models.BooleanField(default=True, verbose_name="Is_Availabel")
    product_image=models.ImageField(upload_to='image')

    def __str__(self):
        return self.name

class Cart(models.Model):
    userid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='userid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class Order(models.Model):
    order_id=models.CharField(max_length=50)
    user_id=models.ForeignKey("auth.User",on_delete=models.CASCADE,db_column="user_id")
    p_id=models.ForeignKey("Product",on_delete=models.CASCADE,db_column="p_id")
    qty=models.IntegerField(default=1)
    amt=models.FloatField()

    def __str__(self):
        return self.order_id