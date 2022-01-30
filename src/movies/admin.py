from django.contrib import admin
from .models import WatchDay, ShowTime, Movies,TicketBooking,Audience
# Register your models here.

admin.site.register(WatchDay)
admin.site.register(Movies)
admin.site.register(ShowTime)
admin.site.register(Audience)
admin.site.register(TicketBooking)