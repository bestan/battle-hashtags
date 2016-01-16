from django.contrib import admin
from battle.models import Battle, BattleHashtags, Hashtag

class BattleHashtagsInline(admin.TabularInline):
    model = BattleHashtags
    fields = ['hashtag']

class HashtagAdmin(admin.ModelAdmin):
    inline = [
        BattleHashtagsInline
    ]

class BattleAdmin(admin.ModelAdmin):
    fields = ('name', 'start_time', 'end_time')
    inlines = [
        BattleHashtagsInline
    ]

admin.site.register(Battle, BattleAdmin)
admin.site.register(Hashtag, HashtagAdmin)
