from django.contrib.auth.models import User
from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=60) # Field name made lowercase.
    class Meta:
        db_table = u'Country'
        
    def __unicode__(self):
        return self.name

class City(models.Model):
    id_country = models.ForeignKey(Country) # Field name made lowercase.
    name = models.CharField(max_length=60) # Field name made lowercase.
    class Meta:
        db_table = u'City'
        
    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    bulletins = models.BooleanField() # Field name made lowercase.
    email_2 = models.EmailField(max_length=90, blank=True) # Field name made lowercase.
    phone_1 = models.CharField(max_length=30, blank=True) # Field name made lowercase.
    phone_2 = models.CharField(max_length=30, blank=True) # Field name made lowercase.
    lang = models.IntegerField(null=True, blank=True) # Field name made lowercase.
    img = models.CharField(max_length=50L, blank=True) # Field name made lowercase.
    fb_token = models.CharField(max_length=450, blank=True) # Field name made lowercase.
    tw_token = models.CharField(max_length=480, blank=True) # Field name made lowercase.
    city = models.ForeignKey(City, null=True, blank=True) # Field name made lowercase.
    level = models.IntegerField(default='0') # Field name made lowercase.
    rating = models.IntegerField(default='0') # Field name made lowercase.
    ranking_qty = models.IntegerField(null=True, blank=True, default='0') # Field name made lowercase.
    quds = models.IntegerField(default='0') # Field name made lowercase.
    follower_qty = models.IntegerField(default='0') # Field name made lowercase.
    followed_qty = models.IntegerField(default='0') # Field name made lowercase.
    barter_qty = models.IntegerField(default='0') # Field name made lowercase.
    remaining_invitations = models.IntegerField(default='15') # Field name made lowercase.
    art = models.BooleanField(default=False) # Field name made lowercase.
    music = models.BooleanField(default=False) # Field name made lowercase.
    tech = models.BooleanField(default=False) # Field name made lowercase.
    cars = models.BooleanField(default=False) # Field name made lowercase.
    travels = models.BooleanField(default=False) # Field name made lowercase.
    clothes = models.BooleanField(default=False) # Field name made lowercase.
    cine = models.BooleanField(default=False) # Field name made lowercase.
    sports = models.BooleanField(default=False) # Field name made lowercase.
    eco = models.BooleanField(default=False) # Field name made lowercase.
    culture = models.BooleanField(default=False) # Field name made lowercase.
    spectacles = models.BooleanField(default=False) # Field name made lowercase.
    love = models.BooleanField(default=False) # Field name made lowercase.
    food = models.BooleanField(default=False) # Field name made lowercase.
    vacations = models.BooleanField(default=False) # Field name made lowercase.
    services = models.BooleanField(default=False) # Field name made lowercase.
    class Meta:
        db_table = u'UserProfile'
    
    def __unicode__(self):
        return self.user.get_full_name()
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
    
class Rating(models.Model):
    id_rater = models.ForeignKey(User, null=True, related_name='rating_rater', blank=True) # Field name made lowercase.
    id_rated = models.ForeignKey(User, related_name='rating_rated') # Field name made lowercase.
    level = models.IntegerField() # Field name made lowercase.
    datetime = models.DateTimeField() # Field name made lowercase.
    class Meta:
        db_table = u'Rating'
    
    def __unicode__(self):
        return self.id_rater.get_full_name() + " to " + self.id_rated.get_full_name() 
    

class Followers(models.Model):  
    id_follower = models.ForeignKey(User, primary_key=True, related_name='followers_follower') # Field name made lowercase.
    id_followed = models.ForeignKey(User, related_name='followers_followed') # Field name made lowercase.
    class Meta:
        db_table = u'Followers'
    
    def __unicode__(self):
        return self.id_follower.get_full_name() + " to " + self.id_followed.get_full_name() 
    

class WarningReason(models.Model):
    text = models.CharField(max_length=150) # Field name made lowercase.
    class Meta:
        db_table = u'WarningReason'
        
    def __unicode__(self):
        return self.name

class Warning(models.Model):
    id_sender = models.ForeignKey(User, related_name='warning_sender') # Field name made lowercase.
    id_receiver = models.ForeignKey(User, related_name='warning_receiver') # Field name made lowercase.
    reason = models.ForeignKey(WarningReason, null=True, blank=True) # Field name made lowercase.
    message = models.TextField() # Field name made lowercase.
    datetime = models.IntegerField() # Field name made lowercase.
    class Meta:
        db_table = u'Warning'
    
    def __unicode__(self):
        return self.id_sender.get_full_name() + " to " + self.id_receiver.get_full_name() 

class Lang(models.Model):
    name = models.CharField(max_length=20L) # Field name made lowercase.
    class Meta:
        db_table = 'Lang'
    
    def __unicode__(self):
        return self.name
