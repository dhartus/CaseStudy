from django.db import models

# Create your models here.

class RetailStore(models.Model):
    id = models.AutoField(primary_key=True)
    store_id = models.IntegerField(blank=False)
    sku = models.CharField(max_length=50,blank=False)
    product_name = models.CharField(max_length=50,blank=False)
    price = models.IntegerField(blank=False)
    date = models.DateField(blank=False)


