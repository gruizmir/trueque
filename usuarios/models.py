# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Country(models.Model):
    id_country = models.IntegerField(primary_key=True, db_column='ID_country') # Field name made lowercase.
    country_name = models.CharField(max_length=60, db_column='Country_name') # Field name made lowercase.
    class Meta:
        db_table = u'Country'

class City(models.Model):
    id_city = models.IntegerField(primary_key=True, db_column='ID_city') # Field name made lowercase.
    id_country = models.ForeignKey(Country, db_column='ID_country') # Field name made lowercase.
    city_name = models.CharField(max_length=60, db_column='City_name') # Field name made lowercase.
    class Meta:
        db_table = u'City'

class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True, db_column='ID_usuario') # Field name made lowercase.
    usuario_password = models.CharField(max_length=75, db_column='Usuario_password') # Field name made lowercase.
    usuario_name = models.CharField(max_length=60, db_column='Usuario_name') # Field name made lowercase.
    usuario_lastname = models.CharField(max_length=60, db_column='Usuario_lastname') # Field name made lowercase.
    usuario_bulletins = models.BooleanField(db_column='Usuario_bulletins') # Field name made lowercase.
    usuario_email_1 = models.EmailField(max_length=90, unique=True, db_column='Usuario_email_1') # Field name made lowercase.
    usuario_email_2 = models.EmailField(max_length=90, db_column='Usuario_email_2', blank=True) # Field name made lowercase.
    usuario_phone_1 = models.CharField(max_length=30, db_column='Usuario_phone_1', blank=True) # Field name made lowercase.
    usuario_phone_2 = models.CharField(max_length=30, db_column='Usuario_phone_2', blank=True) # Field name made lowercase.
    usuario_language = models.CharField(max_length=15, db_column='Usuario_language', blank=True) # Field name made lowercase.
    usuario_fb_token = models.CharField(max_length=450, db_column='Usuario_FB_Token', blank=True) # Field name made lowercase.
    usuario_tw_token = models.CharField(max_length=480, db_column='Usuario_TW_Token', blank=True) # Field name made lowercase.
    usuario_register_date = models.DateTimeField(db_column='Usuario_register_date') # Field name made lowercase.
    usuario_city = models.ForeignKey(City, null=True, db_column='Usuario_city', blank=True) # Field name made lowercase.
    usuario_level = models.IntegerField(db_column='Usuario_level', default='0') # Field name made lowercase.
    usuario_rating = models.IntegerField(db_column='Usuario_rating', default='0') # Field name made lowercase.
    usuario_ranking_qty = models.IntegerField(null=True, db_column='Usuario_ranking_qty', blank=True, default='0') # Field name made lowercase.
    usuario_quds = models.IntegerField(db_column='Usuario_quds', default='0') # Field name made lowercase.
    usuario_follower_qty = models.IntegerField(db_column='Usuario_follower_qty', default='0') # Field name made lowercase.
    usuario_followed_qty = models.IntegerField(db_column='Usuario_followed_qty', default='0') # Field name made lowercase.
    usuario_barter_qty = models.IntegerField(db_column='Usuario_barter_qty', default='0') # Field name made lowercase.
    usuario_remaining_invitations = models.IntegerField(db_column='Usuario_remaining_invitations', default='15') # Field name made lowercase.
    usuario_active = models.BooleanField(db_column='Usuario_active', default=False)
    usuario_art = models.BooleanField(db_column='Usuario_art') # Field name made lowercase.
    usuario_music = models.BooleanField(db_column='Usuario_music') # Field name made lowercase.
    usuario_tech = models.BooleanField(db_column='Usuario_tech') # Field name made lowercase.
    usuario_cars = models.BooleanField(db_column='Usuario_cars') # Field name made lowercase.
    usuario_travels = models.BooleanField(db_column='Usuario_travels') # Field name made lowercase.
    usuario_clothes = models.BooleanField(db_column='Usuario_clothes') # Field name made lowercase.
    usuario_cine = models.BooleanField(db_column='Usuario_cine') # Field name made lowercase.
    usuario_sports = models.BooleanField(db_column='Usuario_sports') # Field name made lowercase.
    usuario_eco = models.BooleanField(db_column='Usuario_eco') # Field name made lowercase.
    usuario_culture = models.BooleanField(db_column='Usuario_culture') # Field name made lowercase.
    usuario_spectacles = models.BooleanField(db_column='Usuario_spectacles') # Field name made lowercase.
    usuario_love = models.BooleanField(db_column='Usuario_love') # Field name made lowercase.
    usuario_food = models.BooleanField(db_column='Usuario_food') # Field name made lowercase.
    usuario_vacations = models.BooleanField(db_column='Usuario_vacations') # Field name made lowercase.
    usuario_services = models.BooleanField(db_column='Usuario_services') # Field name made lowercase.
    class Meta:
        db_table = u'Usuario'

class Rating(models.Model):
    id_rating = models.IntegerField(primary_key=True, db_column='ID_rating') # Field name made lowercase.
    id_rater = models.ForeignKey(Usuario, null=True, db_column='ID_rater', related_name='rating_rater', blank=True) # Field name made lowercase.
    id_rated = models.ForeignKey(Usuario, db_column='ID_rated', related_name='rating_rated') # Field name made lowercase.
    rating_level = models.IntegerField(db_column='Rating_level') # Field name made lowercase.
    rating_datetime = models.DateTimeField(db_column='Rating_datetime') # Field name made lowercase.
    class Meta:
        db_table = u'Rating'

class Followers(models.Model):
    id_follower = models.ForeignKey(Usuario, primary_key=True, db_column='ID_follower', related_name='followers_follower') # Field name made lowercase.
    id_followed = models.ForeignKey(Usuario, db_column='ID_followed', related_name='followers_followed') # Field name made lowercase.
    class Meta:
        db_table = u'Followers'

class Warningreason(models.Model):
    id_reason = models.IntegerField(primary_key=True, db_column='ID_reason') # Field name made lowercase.
    reason_text = models.CharField(max_length=150, db_column='Reason_text') # Field name made lowercase.
    class Meta:
        db_table = u'WarningReason'

class Warning(models.Model):
    id_warning = models.IntegerField(primary_key=True, db_column='ID_warning') # Field name made lowercase.
    id_sender = models.ForeignKey(Usuario, db_column='ID_sender', related_name='warning_sender') # Field name made lowercase.
    id_receiver = models.ForeignKey(Usuario, db_column='ID_receiver', related_name='warning_receiver') # Field name made lowercase.
    warning_reason = models.ForeignKey(Warningreason, null=True, db_column='Warning_reason', blank=True) # Field name made lowercase.
    warning_message = models.TextField(db_column='Warning_message') # Field name made lowercase.
    warning_datetime = models.IntegerField(db_column='Warning_datetime') # Field name made lowercase.
    class Meta:
        db_table = u'Warning'
