from django.contrib import admin
from models import Profile

# Register your models here.
admin.site.register(Profile,
    search_fields=('user__id', 'first_name', 'last_name'),
    list_display=('first_name', 'last_name', 'mu', 'sigma'),
    list_display_links=('first_name', 'last_name','mu', 'sigma'),
)

