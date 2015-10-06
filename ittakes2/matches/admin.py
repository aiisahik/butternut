from django.contrib import admin

from models import Match

admin.site.register(Match,
    search_fields=('winner__first_name', 'winner__last_name', 'loser__last_name', 'winner__first_name'),
    list_display=('create_date', 'winner', 'winner_mu', 'loser', 'loser_mu'),
    list_display_links=('winner', 'loser', 'create_date'),
    list_filter = ('winner', 'loser')
)
# Register your models here.
