from django.contrib import admin
from usuarios.models import Country, City, UserProfile,Warning,Lang,WarningReason,Followers, Rating

admin.site.register(Country)
admin.site.register(City)
admin.site.register(UserProfile)
admin.site.register(Warning)
admin.site.register(Lang)
admin.site.register(WarningReason)
admin.site.register(Followers)
admin.site.register(Rating)
