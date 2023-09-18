from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import ScoreCardTitle,ScoreCard
# Register your models here.
User = get_user_model()

class ScoreCardTitleAdmin(admin.StackedInline):
    model = ScoreCardTitle
    extra = 0

class ScoreCardAdmin(admin.ModelAdmin):
    inlines = [ScoreCardTitleAdmin]
    list_display = ['name','user']
    readonly_fields = ['timestamp','updated']
    raw_id_fields = ['user']


admin.site.register(ScoreCard ,ScoreCardAdmin)
admin.site.register(ScoreCardTitle)