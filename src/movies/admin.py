from django.contrib import admin
from .models import WatchDay, ShowTime, Movies
# Register your models here.

admin.site.register(WatchDay)
admin.site.register(Movies)
admin.site.register(ShowTime)