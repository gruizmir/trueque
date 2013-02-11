from django.db import models
from usuarios.models import Usuario

class Product(models.Model):
    id_product = models.IntegerField(primary_key=True, db_column='ID_product') # Field name made lowercase.
    id_owner = models.ForeignKey(Usuario, db_column='ID_owner') # Field name made lowercase.
    product_name = models.CharField(max_length=90, db_column='Product_name') # Field name made lowercase.
    product_img = models.CharField(max_length=300, db_column='Product_img') # Field name made lowercase.
    product_description = models.TextField(db_column='Product_description', blank=True) # Field name made lowercase.
    product_q_amount = models.IntegerField(db_column='Product_Q_amount') # Field name made lowercase.
    product_datetime = models.DateTimeField(db_column='Product_datetime') # Field name made lowercase.
    product_follower_qty = models.IntegerField(db_column='Product_follower_qty') # Field name made lowercase.
    product_visit_qty = models.IntegerField(db_column='Product_visit_qty') # Field name made lowercase.
    product_country = models.CharField(max_length=60, db_column='Product_country') # Field name made lowercase.
    product_city = models.CharField(max_length=60, db_column='Product_city') # Field name made lowercase.
    class Meta:
        db_table = u'Product'

class Category(models.Model):
    id_category = models.IntegerField(primary_key=True, db_column='ID_category') # Field name made lowercase.
    category_name = models.CharField(max_length=60, db_column='Category_name') # Field name made lowercase.
    class Meta:
        db_table = u'Category'

class ProductCategory(models.Model):
    id_product = models.ForeignKey(Product, primary_key=True, db_column='ID_product') # Field name made lowercase.
    id_category = models.ForeignKey(Category, db_column='ID_category') # Field name made lowercase.
    class Meta:
        db_table = u'Product_category'
