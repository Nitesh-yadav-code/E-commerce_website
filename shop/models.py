from django.db import models

# Create your models here.


class myProduct(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50, default="")
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc =models.CharField(max_length=300, default="")
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")
    def __str__(self):
        return self.product_name


class contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70, default="")
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=50, default="")
    desc =models.CharField(max_length=500, default="")
    def __str__(self):
        return self.name


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    email = models.CharField(max_length=70, default="")
    name = models.CharField(max_length=70, default="")
    address =models.CharField(max_length=500, default="")
    phone = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=80, default="")
    state = models.CharField(max_length=80, default="")
    zip_code = models.CharField(max_length=80, default="")
    def __str__(self):
        return self.name


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp  = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.update_desc[0:10] + "..."