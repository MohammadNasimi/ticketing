from django.contrib import admin

# Register your models here.
from ticketing.models import TicketAnswer,Ticket

admin.site.register(Ticket)
admin.site.register(TicketAnswer)
