from django.db import models

class Precios(models.Model):
    bajo = models.IntegerField(db_column='Bajo') # Field name made lowercase.
    alto = models.IntegerField(db_column='Alto') # Field name made lowercase.
    precio_datetime = models.DateTimeField(primary_key=True, db_column='Precio_datetime') # Field name made lowercase.
    class Meta:
        db_table = u'Precios'
